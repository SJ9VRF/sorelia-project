# Experiment registry

This registry distinguishes **executed engineering evidence** from **paper-scale pending work**.

| Experiment | Purpose | Status | Primary artifact |
|---|---|---|---|
| Local end-to-end loop | Verify closed-loop execution | Executed | `artifacts/v110_smoke/` |
| Chromium fixture | Verify real browser DOM/action/recovery path | Executed | `artifacts/browser_smoke.json` |
| Equal-budget curriculum comparison | Check comparison contract/baselines | Executed smoke | `artifacts/v100_compare.json` |
| Repeated-trial multiseed | Check uncertainty/statistics path | Executed smoke | `artifacts/v070_release_multiseed.json` |
| Static-priority baseline | Separate frontier dynamics from static failure scoring | Executed | comparison harness/tests |
| Shuffled-label control | Test dependence on semantic failure labels | Executed smoke | ablation harness |
| Random-cluster control | Test dependence on meaningful clustering | Executed smoke | ablation harness |
| Leakage gate | Prevent train/eval contamination | Executed | pipeline/tests |
| Human mechanism calibration | Validate automatic matching vs humans | Infrastructure ready; annotations pending | annotation packet/scorer |
| Real trainable VLM post-training | Test scientific hypothesis on real agents | Pending external compute/model | paper-scale protocol |
| Held-out website/application families | Test ecological transfer | Pending | paper-scale protocol |
| 5+ training seeds × repeated eval trials | Main statistical evidence | Pending | paper-scale protocol |
| Published-agent head-to-head | Establish comparative performance | Pending | paper-scale protocol |

A pending experiment must not be cited as completed evidence.
