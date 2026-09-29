# EXP-003 — Moving failure-frontier smoke

**Evidence tier:** engineering smoke / methodology validation, not frontier-model performance evidence.

## Hypothesis
Can a policy update leave success unchanged while shifting reliability risk?

## Setup
Local closed-loop smoke with mechanism matching across updates.

## Result
At iteration 2, task success stayed at 0.90 while risk introduced (0.5949) exceeded risk removed (0.4485), displacement ratio 1.3263.

## Interpretation
Aggregate success hid an adverse redistribution of failure risk.

## Next decision
Promote risk displacement and mechanism transition states to core SORELIA outputs.
