import pytest

from sorelia.benchmarks.tasks import make_tasks
from sorelia.infra.rollout import run_task
from sorelia.benchmarks.sandbox import InteractiveSandbox


class FailingAgent:
    model_id = 'provider'
    version = 'v1'
    def act(self, context):
        raise RuntimeError('provider unavailable')


class TrackingEnv(InteractiveSandbox):
    closed = False
    def close(self):
        type(self).closed = True


def test_environment_closes_when_model_backend_raises():
    TrackingEnv.closed = False
    with pytest.raises(RuntimeError, match='provider unavailable'):
        run_task(FailingAgent(), make_tasks(1, seed=9)[0], env_factory=TrackingEnv)
    assert TrackingEnv.closed is True
