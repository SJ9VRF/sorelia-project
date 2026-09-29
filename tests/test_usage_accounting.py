from sorelia.infra.rollout import run_task
from sorelia.schema import AgentDecision
from sorelia.benchmarks.tasks import make_tasks
from sorelia.features import correct_action


class MeasuredAgent:
    model_id = "measured"
    version = "v1"
    def act(self, context):
        return AgentDecision(
            action=correct_action(context.task, context.step),
            input_tokens=5,
            output_tokens=2,
            model_latency_ms=3.5,
            monetary_cost=.01,
        )


class StringAgent:
    model_id = "string"
    version = "v1"
    def act(self, context):
        return correct_action(context.task, context.step)


def test_measured_usage_is_aggregated():
    t = make_tasks(1, seed=3)[0]
    tr = run_task(MeasuredAgent(), t)
    assert tr.usage_known is True
    assert tr.cost_known is True
    assert tr.tokens == tr.input_tokens + tr.output_tokens
    assert tr.tokens > 0
    assert tr.monetary_cost > 0
    assert tr.model_latency_ms > 0


def test_bare_string_agent_does_not_invent_usage():
    t = make_tasks(1, seed=4)[0]
    tr = run_task(StringAgent(), t)
    assert tr.tokens == 0
    assert tr.monetary_cost == 0
    assert tr.usage_known is False
    assert tr.cost_known is False
