# Truth audit

## Executed and verified in this release

- source-tree test suite
- end-to-end state-machine SORELIA loop
- fixed-budget baseline comparison using the actual moving-frontier SORELIA scheduler
- equal verified-data budget enforcement across all compared curricula
- run manifests with config/source hashes and evidence indexes
- claim-to-evidence release audit
- five-seed synthetic smoke harness
- bootstrap/statistical utilities
- provenance and duplicate filtering
- correction/preference dataset construction
- real Chromium + Playwright local fixture execution
- state-based browser grading
- browser rollback/recovery path

## Implemented but not evidence for frontier-agent claims

- failure-conditioned curriculum scheduler
- UCB allocation scheduler
- synthetic counterfactual generator
- browser adapter contract

These components are executable, but their existence does not prove that they improve a frontier agent.

## Not executed / not claimed

- training or fine-tuning a frontier VLM/LLM
- external website computer-use benchmark
- hundreds of independently authored browser tasks
- human annotation/calibration study
- paper-scale ablation matrix
- held-out-site-family generalization
- GPU-scale RL
- statistically supported superiority of SORELIA over strong baselines

A public paper or résumé must not convert any item in this last section into a completed result until the corresponding experiment is actually run.
