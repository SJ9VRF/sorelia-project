# Provider Integration — v1.1.0

SORELIA keeps provider SDKs outside the research core but ships optional, testable adapters for two common API shapes:

- `OpenAIResponsesAgent` — OpenAI Responses API
- `AnthropicMessagesAgent` — Anthropic Messages API

These adapters are **implemented and offline-tested with injected fake clients**. The released evidence does not claim that proprietary provider models were executed.

## Install

```bash
pip install -e '.[openai]'
# or
pip install -e '.[anthropic]'
# or
pip install -e '.[providers]'
```

Credentials are read from `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`. `sorelia doctor` reports only whether credentials are present; it never prints them.

## Strict action contract

Provider output must be strict JSON:

```json
{"action": "..."}
```

Malformed outputs raise an infrastructure/model-interface error instead of being silently converted into task failures. This prevents parsing failures from contaminating the scientific failure taxonomy.

## Usage accounting

A provider adapter returns `AgentDecision`, which can carry measured:

- input tokens
- output tokens
- model-call latency
- monetary cost, **only if an explicit cost estimator is supplied**

SORELIA intentionally does not hard-code provider prices. Prices change; a stale pricing table would create misleading cost metrics. If cost is unavailable, `cost_known=false` and aggregate cost metrics are `null`, not zero.

Local/replay agents may still return a bare string action. Their usage is recorded as unavailable rather than estimated.

## What is not claimed

The presence of provider adapters is integration evidence, not frontier-model experimental evidence. Paper claims still require the real-agent gates in `PAPER_READINESS.md`.
