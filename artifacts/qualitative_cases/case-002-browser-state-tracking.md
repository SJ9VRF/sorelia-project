# Case 002 — Repeated state-tracking failure in Chromium fixture

**Source:** `artifacts/failure_examples/browser-real-0001.json`.

The retained browser trajectory repeatedly selects an incorrect action, corrupts state, and records the local correction required to restore progress. The first event is:

- selected action: `B`
- expected correction: `C`
- failure type: `state_tracking`
- severity: 0.6
- recoverability: 0.7

The important artifact is not that recovery succeeds; it is that the raw trajectory, expected state, observed state, correction action, and downstream effect are all retained for audit.
