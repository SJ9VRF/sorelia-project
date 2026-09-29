from __future__ import annotations
import argparse
import json
from .pipeline import run_experiment
from .experiments import compare
from .experiments_multiseed import run_multiseed
from .audit import audit_repository
from .experiments_ablation import run_ablations
from .analysis.calibration import build_matching_annotation_packet, write_annotation_packet, cohen_kappa, calibrate_matcher
from .doctor import doctor


def main():
    p = argparse.ArgumentParser(prog="sorelia")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="Run an end-to-end SORELIA experiment")
    r.add_argument("--config", required=True)
    r.add_argument("--out", required=True)

    c = sub.add_parser("compare", help="Run fixed-budget curriculum baselines")
    c.add_argument("--config", required=True)
    c.add_argument("--out", required=True)

    m = sub.add_parser("multiseed", help="Run fixed-budget baselines across multiple seeds with bootstrap CIs")
    m.add_argument("--config", required=True)
    m.add_argument("--out", required=True)

    ab = sub.add_parser("ablate", help="Run executable core SORELIA ablations")
    ab.add_argument("--config", required=True)
    ab.add_argument("--out", required=True)

    a = sub.add_parser("audit", help="Audit claim-to-evidence and public release integrity")
    a.add_argument("--root", default=".")

    cp = sub.add_parser("calibration-packet", help="Export a blank human matching-calibration packet from a frontier report")
    cp.add_argument("--frontier", required=True)
    cp.add_argument("--out", required=True)

    d = sub.add_parser("doctor", help="Report runtime readiness for core and optional browser integrations")

    cs = sub.add_parser("calibration-score", help="Score two completed matching-annotation packets and model calibration")
    cs.add_argument("--annotator-a", required=True)
    cs.add_argument("--annotator-b", required=True)

    args = p.parse_args()
    if args.cmd == "run":
        results = run_experiment(args.config, args.out)
        print(json.dumps(results["history"], indent=2))
    elif args.cmd == "compare":
        print(json.dumps(compare(args.config, args.out), indent=2))
    elif args.cmd == "multiseed":
        print(json.dumps(run_multiseed(args.config, args.out)["summary"], indent=2))
    elif args.cmd == "ablate":
        print(json.dumps(run_ablations(args.config, args.out)["summary"], indent=2))
    elif args.cmd == "audit":
        result = audit_repository(args.root)
        print(json.dumps(result, indent=2))
        if not result["ok"]:
            raise SystemExit(2)
    elif args.cmd == "calibration-packet":
        frontier = json.load(open(args.frontier, "r", encoding="utf-8"))
        packet = build_matching_annotation_packet(frontier)
        write_annotation_packet(args.out, packet)
        print(json.dumps({"pairs": len(packet), "out": args.out}, indent=2))
    elif args.cmd == "doctor":
        print(json.dumps(doctor(), indent=2))
    elif args.cmd == "calibration-score":
        def read_jsonl(path):
            with open(path, "r", encoding="utf-8") as f:
                return [json.loads(line) for line in f if line.strip()]
        aa, bb = read_jsonl(args.annotator_a), read_jsonl(args.annotator_b)
        print(json.dumps({"agreement": cohen_kappa(aa, bb), "matcher_vs_a": calibrate_matcher(aa), "matcher_vs_b": calibrate_matcher(bb)}, indent=2))

if __name__ == "__main__":
    main()
