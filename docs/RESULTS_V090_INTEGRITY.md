# v0.9 integrity / negative-control engineering smoke

This is **engineering evidence only**, not a real-agent scientific result.

Configuration: 2 iterations, 24 training tasks, 24 IID evaluation tasks, 12 shifted/stress tasks, 2 evaluation trials/task, 32 verified training tasks/iteration.

## End-to-end integrity run

Final local end-to-end metrics included:

- IID task success: **0.9167**
- exact train/eval leakage: **0**
- near-duplicate train/eval pairs at the local diagnostic threshold: **0**
- matching ambiguous rate: **0.25**
- frontier net risk change: **-0.1696**
- risk displacement ratio: **0.5677**

The 25% ambiguous-match rate is not treated as validated uncertainty calibration. It motivates the human protocol in `docs/HUMAN_CALIBRATION_PROTOCOL.md`.

## Executable ablation / negative-control smoke

| Variant | IID success | Stress success | Failures/task | Exact eval leakage |
|---|---:|---:|---:|---:|
| Full SORELIA | 0.8750 | 0.9167 | 1.0625 | 0 |
| Static priority | 0.9583 | 0.9167 | 0.6042 | 0 |
| No exploration | 0.8542 | 0.8333 | 1.1667 | 0 |
| Single iteration | 0.8750 | 0.8333 | 1.7708 | 0 |
| Shuffled failure labels | 0.9167 | 0.9167 | 0.8333 | 0 |
| Random cluster assignment | 0.9583 | 0.8750 | 0.9375 | 0 |

The toy environment does **not** support a SORELIA superiority claim. Static priority and random-cluster assignment are stronger on IID success in this run. The correct interpretation is that the falsification machinery executes and that the central thesis remains open for the real-agent study.
