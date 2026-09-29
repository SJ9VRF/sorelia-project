# Usage and Cost Accounting

SORELIA separates **measured zero** from **unknown**.

A trajectory records:

- `input_tokens`, `output_tokens`, `tokens`
- `usage_known`
- `model_latency_ms`
- `monetary_cost`
- `cost_known`

Aggregate metrics include `usage_coverage` and `cost_coverage`. If no trajectory has measured cost, `mean_cost` and `cost_per_success` are `null`. The harness never invents token counts or prices for local agents.

This policy is intentionally conservative because cost/latency comparisons can otherwise look quantitative while being based on fabricated accounting.
