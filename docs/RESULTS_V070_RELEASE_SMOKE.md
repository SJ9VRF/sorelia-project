# v0.7.0 repeated-trial release smoke

This is an **engineering smoke test**, not a paper result and not evidence of state-of-the-art performance.

Configuration: 3 training seeds, 36 held-out synthetic tasks, 2 evaluation trials/task, 3 curriculum iterations, equal verified-data budget (48/iteration).

Final mean task success:

| curriculum | mean task success |
|---|---:|
| random | 0.9861 |
| human-balanced | 0.9630 |
| difficulty | 0.9583 |
| SORELIA | 0.9491 |
| frequency | 0.9444 |

The paired SORELIA-minus-random mean delta was -0.0370. The paired bootstrap interval included zero (approximately [-0.0833, 0.0000]) and the paired randomization p-value was approximately 0.493. With only three seeds, this smoke run is intentionally underpowered and supports **no superiority claim**.

Why retain an adverse/null smoke result? Because the artifact should demonstrate that its evaluation machinery can falsify the desired hypothesis. The research claim remains open until paper-scale real-agent experiments are completed.

Raw evidence: `artifacts/v070_release_multiseed.json`.
