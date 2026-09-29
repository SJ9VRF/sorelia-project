from types import SimpleNamespace

from sorelia.adapters.provider_agents import OpenAIResponsesAgent, AnthropicMessagesAgent
from sorelia.schema import DecisionContext, Task


def ctx():
    task = Task("t", "browser", "grounding", .2, 2, {}, "do it", 1)
    return DecisionContext(task, 0, {"step": 0}, {"completed": 1})


class FakeOpenAIClient:
    class responses:
        @staticmethod
        def create(**kwargs):
            return SimpleNamespace(
                id="r1", output_text='{"action":"a1"}',
                usage=SimpleNamespace(input_tokens=11, output_tokens=3),
            )


def test_openai_adapter_usage_and_cost():
    a = OpenAIResponsesAgent(model="test-openai", client=FakeOpenAIClient(), cost_estimator=lambda i,o: i*.1+o*.2)
    d = a.act(ctx())
    assert d.action == "a1"
    assert (d.input_tokens, d.output_tokens) == (11, 3)
    assert abs(d.monetary_cost - 1.7) < 1e-12


class FakeAnthropicClient:
    class messages:
        @staticmethod
        def create(**kwargs):
            return SimpleNamespace(
                id="m1", content=[SimpleNamespace(text='{"action":"a2"}')],
                usage=SimpleNamespace(input_tokens=7, output_tokens=2),
            )


def test_anthropic_adapter_usage():
    a = AnthropicMessagesAgent(model="test-anthropic", client=FakeAnthropicClient())
    d = a.act(ctx())
    assert d.action == "a2"
    assert (d.input_tokens, d.output_tokens) == (7, 2)
    assert d.monetary_cost is None
