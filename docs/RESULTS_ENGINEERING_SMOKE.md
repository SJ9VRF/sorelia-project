# Engineering smoke results

These results validate that the SORELIA implementation executes. They are **not** paper-scale claims about frontier computer-use models.

## Local state-machine loop

The three-iteration local run produced explicit frontier-transition artifacts. In the final transition, the mechanism tracker identified a mixture of emergent, contracting, persistent and extinct failure mechanisms. This demonstrates that the moving-frontier analysis is executable rather than decorative.

See `artifacts/sorelia_smoke/metrics.json` and `frontier_i*.json` for the exact run.

## Chromium / Playwright fixture

A 12-task isolated real-browser smoke test produced:

- task success: 0.5833
- mean partial success: 0.7431
- failure events: 54
- recovery attempts: 27
- recovery success within the fixture: 1.0
- catastrophic-action rate: 0.0833

The purpose is only to verify real DOM/action/state integration. The fixture is intentionally small and local, so these numbers must not be used as performance claims.
