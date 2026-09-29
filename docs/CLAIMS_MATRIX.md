# Claims-to-evidence matrix

| Proposed claim | Required evidence | Status |
|---|---|---|
| Failure-conditioned curricula are more sample efficient | Fixed-data curves across >=3 seeds; same base model/optimizer/data count | Not yet claimed |
| Targeted failures recur less often | Failure-family matched pre/post analysis + unrelated-failure negative control | Not yet claimed |
| Gains generalize beyond source tasks | Held-out UI variants, failure variants and environment families | Not yet claimed |
| Adaptation matters | Adaptive multi-round vs static failure curriculum | Harness implemented; paper experiment pending |
| Verification improves data quality | No-verifier ablation + manual audit of generated tasks | Pending |
| Exploration prevents collapse | 100% exploit vs mixed exploration over >=4 iterations | Pending |

A result should not appear in the abstract, homepage hero, or résumé until the corresponding evidence row is complete.
