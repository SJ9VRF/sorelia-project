# v0.5.0 engineering smoke report

These numbers validate execution of the new stable-mechanism frontier machinery. They are **not** paper claims or frontier-model results.

## Iteration 0
- task success: 0.556
- failures/task: 5.208

## Iteration 1
- task success: 0.931
- failures/task: 0.972
- frontier state counts: `{'initial': 8}`
- risk before → after: 0.000 → 0.000
- risk removed: 0.000
- risk introduced: 0.000
- risk displacement ratio: 0.000
- split/merge topology events: 0

## Iteration 2
- task success: 0.931
- failures/task: 0.667
- frontier state counts: `{'contracting': 3, 'emergent': 1, 'expanding': 2, 'extinct': 1, 'persistent': 2}`
- risk before → after: 1.015 → 1.050
- risk removed: 0.341
- risk introduced: 0.377
- risk displacement ratio: 1.103
- split/merge topology events: 5

## Iteration 3
- task success: 0.972
- failures/task: 0.569
- frontier state counts: `{'contracting': 2, 'emergent': 1, 'expanding': 4, 'extinct': 1, 'persistent': 1}`
- risk before → after: 1.050 → 1.089
- risk removed: 0.300
- risk introduced: 0.338
- risk displacement ratio: 1.128
- split/merge topology events: 2

## Interpretation
The local reference environment is intentionally small. The meaningful engineering observation is that the pipeline can preserve mechanism identity across independent clustering rounds, observe topology events, and report cases where introduced/expanded risk offsets removed/contracted risk. These quantities must be validated on real interactive-agent models before they are used as scientific conclusions.