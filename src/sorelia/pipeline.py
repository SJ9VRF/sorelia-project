from __future__ import annotations
from pathlib import Path
import json
from typing import Dict
import numpy as np
import yaml
from .benchmarks.tasks import make_tasks
from .agents.policy import PolicyAgent
from .infra.rollout import run_suite
from .clustering.failures import extract_failure_points, cluster, summarize
from .curriculum.scheduler import allocate_frontier
from .generation.generator import generate_from_clusters
from .generation.verify import filter_verified
from .training.dataset import supervised_examples
from .evals.metrics import compute_metrics
from .data.io import write_jsonl
from .training.preference import correction_records
from .analysis.statistics import failure_distribution, js_divergence, recurrence_rate, paired_success_delta
from .analysis.frontier import cluster_frontier_transition, cluster_status_index
from .analysis.contamination import assert_no_exact_leakage
from .analysis.calibration import build_matching_annotation_packet, write_annotation_packet
from .run_manifest import build_run_manifest, write_run_manifest
from .evidence import write_evidence_index
from .benchmark_manifest import build_benchmark_manifest, write_benchmark_manifest


def _dump_json(path, obj):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def run_experiment(config_path: str, out_dir: str) -> Dict:
    cfg = yaml.safe_load(Path(config_path).read_text())
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    write_run_manifest(out / "run_manifest.json", build_run_manifest(config_path, "sorelia-run", {"out_dir": str(out)}))
    seed = int(cfg.get("seed", 0))
    train_tasks = make_tasks(int(cfg["benchmark"]["train_tasks"]), seed=seed, prefix="train")
    eval_tasks = make_tasks(int(cfg["benchmark"]["eval_tasks"]), seed=seed + 999, prefix="eval")
    write_benchmark_manifest(out / "benchmark_manifest.json", build_benchmark_manifest(train_tasks, eval_tasks))
    agent = PolicyAgent(seed=seed, version="v0")
    history = []
    training_buffer = []

    # Baseline evaluation is held out from curriculum construction.
    baseline_eval = run_suite(agent, eval_tasks, allow_recovery=cfg["rollout"].get("allow_recovery", True))
    previous_eval = baseline_eval
    previous_cluster_summary = None
    base_metrics = compute_metrics(baseline_eval)
    history.append({"iteration": 0, "split": "eval", **base_metrics})
    write_jsonl(out / "eval_v0.jsonl", baseline_eval)

    for iteration in range(1, int((cfg.get("sorelia") or cfg.get("flywheel"))["iterations"]) + 1):
        train_rollouts = run_suite(agent, train_tasks, allow_recovery=cfg["rollout"].get("allow_recovery", True))
        points = extract_failure_points(train_rollouts)
        labels, cluster_meta = cluster(points, k=int(cfg["clustering"]["k"]), seed=seed + iteration)
        summary = summarize(points, labels)
        if previous_cluster_summary is not None:
            frontier = cluster_frontier_transition(previous_cluster_summary, summary, iteration=iteration)
            summary = {int(k): v for k, v in frontier["annotated_after"].items()}
            status_by_cluster = cluster_status_index(frontier)
        else:
            for cid, c in summary.items():
                c["stable_id"] = f"m0_{cid}"
            frontier = {"summary": {"initial": len(summary)}, "risk_before": 0.0, "risk_after": 0.0,
                        "net_risk_change": 0.0, "risk_removed": 0.0, "risk_introduced": 0.0,
                        "risk_displacement_ratio": 0.0, "mechanisms": [], "topology_events": [],
                        "status_by_cluster": {}, "stable_id_by_cluster": {}, "annotated_after": summary}
            status_by_cluster = {}
        allocation = allocate_frontier(
            summary,
            budget=int(cfg["generation"]["budget"]),
            status_by_cluster=status_by_cluster,
            exploration_ratio=float(cfg["curriculum"]["exploration_ratio"]),
        )
        generated = generate_from_clusters(summary, allocation, iteration=iteration, seed=seed)
        verified, rejected = filter_verified(generated)

        # If the current model produces no failures, preserve trainability with exploration data.
        if not verified:
            verified = make_tasks(max(8, int(cfg["generation"]["budget"])), seed=seed + 5000 + iteration, prefix=f"explore{iteration}")

        training_buffer.extend(verified)
        leakage = assert_no_exact_leakage(training_buffer, eval_tasks)
        X, y = supervised_examples(agent, training_buffer)
        new_agent = PolicyAgent(seed=seed + iteration, version=f"v{iteration}")
        new_agent.fit(X, y)
        agent = new_agent

        ev = run_suite(agent, eval_tasks, allow_recovery=cfg["rollout"].get("allow_recovery", True))
        metrics = compute_metrics(ev)
        before_dist = failure_distribution(previous_eval)
        after_dist = failure_distribution(ev)
        delta = paired_success_delta(previous_eval, ev, seed=seed + iteration)
        row = {
            "iteration": iteration, "split": "eval", **metrics,
            "failure_distribution_js": js_divergence(before_dist, after_dist),
            "failure_recurrence_rate": recurrence_rate(previous_eval, ev),
            "paired_success_delta": delta,
            "n_failures_for_curriculum": len(points),
            "n_clusters": cluster_meta["k"],
            "silhouette": cluster_meta["silhouette"],
            "generated": len(generated),
            "verified": len(verified),
            "rejected": len(rejected),
            "frontier_summary": frontier.get("summary", {}),
            "frontier_risk_before": frontier.get("risk_before", 0.0),
            "frontier_risk_after": frontier.get("risk_after", 0.0),
            "frontier_net_risk_change": frontier.get("net_risk_change", 0.0),
            "risk_removed": frontier.get("risk_removed", 0.0),
            "risk_introduced": frontier.get("risk_introduced", 0.0),
            "risk_displacement_ratio": frontier.get("risk_displacement_ratio", 0.0),
            "frontier_topology_events": len(frontier.get("topology_events", [])),
            "exact_eval_leakage": int(leakage["exact_semantic_overlap_count"] + leakage["task_id_overlap_count"]),
            "near_eval_duplicate_pairs": int(leakage["near_duplicate_pair_count"]),
            "matching_ambiguous_rate": float(frontier.get("matching_calibration", {}).get("ambiguous_rate", 0.0)),
        }
        history.append(row)
        write_jsonl(out / f"train_rollouts_i{iteration}.jsonl", train_rollouts)
        write_jsonl(out / f"corrections_i{iteration}.jsonl", correction_records(train_rollouts))
        write_jsonl(out / f"generated_i{iteration}.jsonl", verified)
        write_jsonl(out / f"eval_v{iteration}.jsonl", ev)
        _dump_json(out / f"clusters_i{iteration}.json", summary)
        _dump_json(out / f"allocation_i{iteration}.json", allocation)
        _dump_json(out / f"frontier_i{iteration}.json", frontier)
        packet = build_matching_annotation_packet(frontier)
        write_annotation_packet(out / f"matching_annotation_packet_i{iteration}.jsonl", packet)
        previous_cluster_summary = summary
        previous_eval = ev

    _dump_json(out / "metrics.json", history)
    write_evidence_index(out)
    return {"history": history, "output_dir": str(out)}
