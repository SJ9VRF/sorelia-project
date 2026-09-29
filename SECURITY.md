# Security policy

SORELIA is designed for isolated research environments. Do not run destructive or privileged computer-use tasks against personal, production, payment, or third-party systems.

## Supported scope

- Local deterministic sandbox
- Isolated local Chromium/Playwright fixtures
- Explicitly authorized research environments

## Never commit

- API keys or tokens
- browser profiles or cookies
- private task data
- credentials embedded in trajectories

`SORELIA` intentionally separates provider/infrastructure errors from agent failures. If you find a vulnerability that could expose credentials, escape the sandbox, bypass action-risk controls, or modify grader state, do not publish exploitation details in an issue. Report it privately to the repository maintainer when a public contact channel is available.

## High-risk actions

Deletion, payment, submission, permission changes, external messaging, and irreversible state changes should be mocked or blocked unless an isolated environment explicitly supports them.
