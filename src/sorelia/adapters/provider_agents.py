from __future__ import annotations

import json
import os
import time
from dataclasses import asdict
from typing import Any, Callable, Iterable

from ..schema import AgentDecision, DecisionContext


def _decision_prompt(context: DecisionContext) -> str:
    payload = {
        "task": asdict(context.task),
        "step": context.step,
        "observation": context.observation,
        "expected_state": context.expected_state,
        "recent_actions": context.recent_actions,
        "recent_observations": context.recent_observations,
    }
    return (
        "You are controlling an interactive environment. Choose exactly one next action. "
        "Return strict JSON only, with schema {\"action\": \"...\"}. Do not add prose.\n"
        + json.dumps(payload, sort_keys=True, separators=(",", ":"))
    )


def _parse_action(text: str) -> str:
    try:
        obj = json.loads(text.strip())
    except json.JSONDecodeError as exc:
        raise ValueError("model output must be strict JSON with an 'action' field") from exc
    action = obj.get("action") if isinstance(obj, dict) else None
    if not isinstance(action, str) or not action.strip():
        raise ValueError("model output JSON must contain a non-empty string 'action'")
    return action.strip()


def _usage_value(obj: Any, name: str) -> int:
    value = getattr(obj, name, 0) if obj is not None else 0
    return int(value or 0)


class OpenAIResponsesAgent:
    """Optional OpenAI Responses API adapter.

    The adapter is lazy-imported and accepts an injected client for offline tests. It is
    implementation support, not evidence that a proprietary model was executed.
    """

    def __init__(
        self,
        *,
        model: str = "gpt-5.6-sol",
        client: Any | None = None,
        version: str | None = None,
        cost_estimator: Callable[[int, int], float] | None = None,
    ):
        if client is None:
            try:
                from openai import OpenAI  # type: ignore
            except ImportError as exc:
                raise RuntimeError("Install SORELIA with the 'openai' extra to use OpenAIResponsesAgent") from exc
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.client = client
        self.model_id = model
        self.version = version or model
        self.cost_estimator = cost_estimator

    def act(self, context: DecisionContext) -> AgentDecision:
        started = time.perf_counter()
        response = self.client.responses.create(model=self.model_id, input=_decision_prompt(context))
        latency = (time.perf_counter() - started) * 1000
        text = getattr(response, "output_text", None)
        if not isinstance(text, str):
            raise ValueError("OpenAI response did not expose text via output_text")
        usage = getattr(response, "usage", None)
        inp = _usage_value(usage, "input_tokens")
        out = _usage_value(usage, "output_tokens")
        cost = self.cost_estimator(inp, out) if self.cost_estimator else None
        return AgentDecision(
            action=_parse_action(text),
            input_tokens=inp,
            output_tokens=out,
            model_latency_ms=latency,
            monetary_cost=cost,
            metadata={"provider": "openai", "response_id": getattr(response, "id", None)},
        )


class AnthropicMessagesAgent:
    """Optional Anthropic Messages API adapter with injected-client testability."""

    def __init__(
        self,
        *,
        model: str = "claude-sonnet-5",
        client: Any | None = None,
        version: str | None = None,
        max_tokens: int = 256,
        cost_estimator: Callable[[int, int], float] | None = None,
    ):
        if client is None:
            try:
                from anthropic import Anthropic  # type: ignore
            except ImportError as exc:
                raise RuntimeError("Install SORELIA with the 'anthropic' extra to use AnthropicMessagesAgent") from exc
            client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.client = client
        self.model_id = model
        self.version = version or model
        self.max_tokens = int(max_tokens)
        self.cost_estimator = cost_estimator

    def act(self, context: DecisionContext) -> AgentDecision:
        started = time.perf_counter()
        message = self.client.messages.create(
            model=self.model_id,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": _decision_prompt(context)}],
        )
        latency = (time.perf_counter() - started) * 1000
        blocks: Iterable[Any] = getattr(message, "content", []) or []
        text = "".join(getattr(block, "text", "") for block in blocks if getattr(block, "text", None))
        usage = getattr(message, "usage", None)
        inp = _usage_value(usage, "input_tokens")
        out = _usage_value(usage, "output_tokens")
        cost = self.cost_estimator(inp, out) if self.cost_estimator else None
        return AgentDecision(
            action=_parse_action(text),
            input_tokens=inp,
            output_tokens=out,
            model_latency_ms=latency,
            monetary_cost=cost,
            metadata={"provider": "anthropic", "message_id": getattr(message, "id", None)},
        )
