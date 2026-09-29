# EXP-002 — Chromium browser fixture

**Evidence tier:** engineering smoke / methodology validation, not frontier-model performance evidence.

## Hypothesis
Does the environment abstraction survive a real browser DOM/action loop?

## Setup
12 isolated Chromium tasks using the retained browser fixture and state-based grading.

## Result
58.3% task success; 54 failure events; 27 recovery attempts; all attempted recoveries succeeded. Token/cost coverage remained unknown rather than fabricated.

## Interpretation
The browser path was real enough to expose trajectories and recovery, but far too narrow for a scientific computer-use claim.

## Next decision
Keep it as engineering evidence; require independent real-site tasks for paper-scale claims.
