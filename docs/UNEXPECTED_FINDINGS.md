# Unexpected findings

## 1. Aggregate success can stay flat while risk gets worse
In the retained v1.1 smoke, task success stayed at 90% while risk introduced exceeded risk removed by 1.33×. This became the strongest motivation for reporting risk displacement explicitly.

## 2. Simple baselines remained stubbornly competitive
Static priority, frequency, human-balanced curricula, and even random-cluster negative controls sometimes matched or exceeded SORELIA in the toy harness. Rather than tune the benchmark until the proposed method won, the project retained those outcomes and narrowed the claim boundary.

## 3. Exploration was not monotonically beneficial
The no-exploration ablation sometimes improved IID success. This invalidated the assumption that an exploration reserve should be treated as universally helpful.

## 4. Mechanism identity itself is a measurement problem
Matching ambiguity reached 25% in a retained integrity run and 50% among matched mechanisms in one later local frontier example. This pushed human calibration from a nice-to-have to a required gate.

## 5. Better engineering metrics exposed earlier false precision
Once usage accounting was audited, early fixed token/cost values were recognized as synthetic. Removing them made the artifact less numerically complete but more scientifically honest.

## 6. A methodological bug was more valuable than another feature
The v0.6 audit found that the arm called SORELIA in the comparison path was still using a legacy static allocator. Fixing the benchmark and adding a regression test improved the credibility of every later result more than adding a new model component would have.
