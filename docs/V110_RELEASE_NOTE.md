# SORELIA v1.1.0 release note

v1.1.0 hardens the boundary between research evidence and provider integration.

The previous rollout engine used fixed synthetic token/cost accounting for local actions. That has been removed. Agents may now return an `AgentDecision` containing measured provider usage and model latency. If usage or cost is unavailable, metrics report it as unavailable rather than as a quantitative zero.

The release also ships optional OpenAI Responses and Anthropic Messages adapters. They are tested through injected fake clients, so request/response parsing and usage extraction are executable without API credentials. This release **does not claim proprietary frontier-model runs**.

The complete source-tree suite passes 36 tests and the release reproduction script validates tests, compile, claim/evidence audit, runtime doctor, benchmark identity, leakage invariants, fixed-budget comparison, negative controls, frontier state, calibration packets, and unknown-cost semantics.
