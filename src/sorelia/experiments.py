from __future__ import annotations
from pathlib import Path
import json, random
from typing import Dict, List
import yaml
from .benchmarks.tasks import make_tasks, make_shifted_tasks
from .agents.policy import PolicyAgent
from .infra.rollout import run_suite, run_suite_repeated
from .clustering.failures import extract_failure_points, cluster, summarize
from .curriculum.scheduler import allocate_frontier, allocate
from .curriculum.baselines import random_curriculum, human_balanced_curriculum, difficulty_curriculum, frequency_allocation
from .generation.generator import generate_from_clusters
from .generation.verify import filter_verified
from .training.dataset import supervised_examples
from .evals.metrics import compute_metrics
from .analysis.frontier import cluster_frontier_transition, cluster_status_index
from .analysis.contamination import assert_no_exact_leakage
from .run_manifest import build_run_manifest, write_run_manifest

MODES = ["sorelia", "priority", "frequency", "random", "difficulty", "human"]


def _make_curriculum(mode, summary, budget, iteration, seed, exploration_ratio, status_by_cluster=None):
    if mode == "sorelia":
        alloc = allocate_frontier(summary, budget, status_by_cluster=status_by_cluster or {}, exploration_ratio=exploration_ratio)
        return generate_from_clusters(summary, alloc, iteration, seed), alloc
    if mode == "priority":
        alloc = allocate(summary, budget, exploration_ratio=exploration_ratio)
        return generate_from_clusters(summary, alloc, iteration, seed), alloc
    if mode == "frequency":
        alloc = frequency_allocation(summary, budget)
        return generate_from_clusters(summary, alloc, iteration, seed), alloc
    if mode == "random": return random_curriculum(budget, iteration, seed), {}
    if mode == "difficulty": return difficulty_curriculum(budget, iteration, seed), {}
    if mode == "human": return human_balanced_curriculum(budget, iteration, seed), {}
    raise ValueError(mode)


def run_mode(cfg: Dict, mode: str) -> List[Dict]:
    seed = int(cfg.get("seed", 0))
    train_tasks = make_tasks(int(cfg["benchmark"]["train_tasks"]), seed=seed, prefix="train")
    eval_tasks = make_tasks(int(cfg["benchmark"]["eval_tasks"]), seed=seed + 999, prefix="eval")
    stress_n = int(cfg.get("benchmark", {}).get("stress_eval_tasks", 0))
    stress_tasks = make_shifted_tasks(stress_n, seed=seed + 1999, prefix="stress") if stress_n > 0 else []
    agent = PolicyAgent(seed=seed, version="v0")
    eval_trials = int(cfg.get("benchmark", {}).get("eval_trials", 1))

    def evaluate(a):
        out = compute_metrics(run_suite_repeated(a, eval_tasks, trials=eval_trials))
        if stress_tasks:
            sm = compute_metrics(run_suite_repeated(a, stress_tasks, trials=eval_trials))
            out.update({f"stress_{k}": v for k, v in sm.items() if k != "failure_type_counts"})
        return out

    rows = [{"mode": mode, "iteration": 0, **evaluate(agent)}]
    buffer = []
    previous_cluster_summary = None

    for iteration in range(1, int(cfg["sorelia"]["iterations"]) + 1):
        train_rollouts = run_suite(agent, train_tasks)
        points = extract_failure_points(train_rollouts)
        labels, meta = cluster(points, k=int(cfg["clustering"]["k"]), seed=seed + iteration)
        control = str(cfg.get("experimental_control", "none"))
        if control == "random_cluster_assignment" and len(labels) > 1:
            shuffled = labels.copy()
            rr = random.Random(seed + iteration * 17011)
            vals = shuffled.tolist(); rr.shuffle(vals)
            import numpy as np
            labels = np.asarray(vals, dtype=int)
        summary = summarize(points, labels)
        if control == "shuffled_failure_labels" and len(summary) > 1:
            rr = random.Random(seed + iteration * 19001)
            cids = sorted(summary)
            failure_types = [summary[c]["failure_type"] for c in cids]
            rr.shuffle(failure_types)
            for cid, ft in zip(cids, failure_types):
                summary[cid]["failure_type"] = ft

        # Only SORELIA receives longitudinal frontier state. Baselines remain static by design.
        status_by_cluster = {}
        frontier_summary = {}
        if mode == "sorelia":
            if previous_cluster_summary is not None:
                frontier = cluster_frontier_transition(previous_cluster_summary, summary, iteration=iteration)
                summary = {int(k): v for k, v in frontier["annotated_after"].items()}
                status_by_cluster = cluster_status_index(frontier)
                frontier_summary = frontier.get("summary", {})
            else:
                for cid, c in summary.items():
                    c["stable_id"] = f"m0_{cid}"
                frontier_summary = {"initial": len(summary)}

        budget = int(cfg["generation"]["budget"])
        curr, alloc = _make_curriculum(
            mode, summary, budget, iteration, seed,
            float(cfg["curriculum"]["exploration_ratio"]),
            status_by_cluster=status_by_cluster,
        )
        verified, _ = filter_verified(curr)
        if not verified:
            verified = random_curriculum(budget, iteration, seed + 777)

        # Fixed verified-data budget is an experimental invariant.
        if len(verified) > budget:
            verified = verified[:budget]
        elif len(verified) < budget:
            top_up = random_curriculum(budget - len(verified), iteration, seed + 9000)
            verified.extend(top_up)
        assert len(verified) == budget, f"verified-data budget drift: {len(verified)} != {budget}"

        buffer.extend(verified)
        leakage = assert_no_exact_leakage(buffer, eval_tasks)
        stress_leakage = assert_no_exact_leakage(buffer, stress_tasks) if stress_tasks else None
        X, y = supervised_examples(agent, buffer)
        nxt = PolicyAgent(seed=seed + iteration, version=f"{mode}-v{iteration}")
        nxt.fit(X, y); agent = nxt
        m = evaluate(agent)
        rows.append({
            "mode": mode,
            "iteration": iteration,
            **m,
            "training_tasks_cumulative": len(buffer),
            "verified_training_tasks_this_iteration": len(verified),
            "curriculum_failures": len(points),
            "n_clusters": meta["k"],
            "frontier_summary": frontier_summary if mode == "sorelia" else {},
            "allocation_total": int(sum(alloc.values())) if alloc else budget,
            "exact_eval_leakage": int(leakage["exact_semantic_overlap_count"] + leakage["task_id_overlap_count"]),
            "near_eval_duplicate_pairs": int(leakage["near_duplicate_pair_count"]),
            "exact_stress_leakage": int((stress_leakage or {}).get("exact_semantic_overlap_count", 0) + (stress_leakage or {}).get("task_id_overlap_count", 0)),
            "experimental_control": control,
        })
        if mode == "sorelia":
            previous_cluster_summary = summary
    return rows


def compare(config_path: str, out_path: str) -> List[Dict]:
    cfg = yaml.safe_load(Path(config_path).read_text())
    rows = []
    for mode in MODES:
        rows.extend(run_mode(cfg, mode))
    out = Path(out_path); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    write_run_manifest(out.with_suffix(out.suffix + '.manifest.json'), build_run_manifest(config_path, "fixed-budget-compare", {"modes": MODES}))
    return rows
