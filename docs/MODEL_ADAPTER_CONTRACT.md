# Model Adapter Contract

SORELIA's core evaluation code must not depend on a specific model provider SDK.

## Decision input

Every interactive policy receives a `DecisionContext` with:

- task metadata and instruction
- current environment observation
- expected state for the current step
- bounded recent actions
- bounded recent observations
- deterministic/stochastic intent

This prevents a toy-only API where the policy sees only a task label and step number.

## Provider boundary

`CallableInteractiveAgent` accepts any function that maps the JSON-serializable decision payload to one action string. A provider integration can therefore own authentication, multimodal prompt construction, retries, rate limiting, and response parsing outside the SORELIA research core.

The rollout engine records the adapter's `model_id` and `version` on every trajectory. The core never rewrites those fields to a local-policy constant.

## Optional provider adapters

The research core remains provider-independent, but v1.1.0 ships optional `OpenAIResponsesAgent` and `AnthropicMessagesAgent` adapters under `src/sorelia/adapters/provider_agents.py`. They are lazy-imported, accept injected clients for offline tests, require strict JSON action output, and return measured usage through `AgentDecision`. Their existence does **not** imply that proprietary frontier-model experiments were executed in this release. See `PROVIDER_INTEGRATION.md` and `USAGE_ACCOUNTING.md`.

## Minimal example

```python
from sorelia.adapters.model_agent import CallableInteractiveAgent


def decide(payload):
    observation = payload["observation"]
    # Call a local model or provider API here and return one environment action.
    return "click:save"

agent = CallableInteractiveAgent(
    decide,
    model_id="my-interactive-model",
    version="checkpoint-2026-09-26",
)
```

The example is an integration contract, not evidence that a frontier provider was used in the released experiments.
