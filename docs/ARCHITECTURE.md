# Architecture

## Interfaces

### Environment

A production environment must provide:

- `reset(task) -> observation`
- `observe() -> observation`
- `step(action) -> observation, done, info`
- `verify() -> structured grader results`
- optional checkpoint / rollback

### Agent

A production agent must provide:

- `act(task, state/history) -> action`
- version metadata
- optional uncertainty/log-probability

### Failure representation

Each failure records task family, failure mechanism, state before action, action, expected state, observed state, severity, recoverability, downstream effects and confidence. Production multimodal variants should add screenshot/UI-tree embeddings and structured world-state features.

## Provenance

Every synthetic task should retain:

`trajectory -> failure_event -> failure_cluster -> generated_task -> verification -> dataset -> training_run -> model_version`

This lineage is required for debugging targeted improvements, contamination, and reward hacking.

## Production adapters

The local sandbox is deliberately replaceable. A browser implementation should use an isolated Playwright/Chromium instance with deterministic fixtures. Document, spreadsheet, email and file tasks should operate on local mock services or containers. High-risk actions such as send/delete/payment must never touch live user accounts during research evaluation.
