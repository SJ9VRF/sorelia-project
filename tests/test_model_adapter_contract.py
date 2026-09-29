from sorelia.adapters.model_agent import CallableInteractiveAgent
from sorelia.infra.rollout import run_task
from sorelia.benchmarks.tasks import make_tasks


def test_callable_agent_receives_observation_and_history():
    seen = []
    task = make_tasks(1, seed=44)[0]
    def decide(payload):
        seen.append(payload)
        # sandbox exposes target through expected state only indirectly; choose a valid action deterministically
        return "A"
    agent = CallableInteractiveAgent(decide, model_id="contract-test", version="v1")
    tr = run_task(agent, task, allow_recovery=True)
    assert seen
    assert "observation" in seen[0] and "expected_state" in seen[0]
    assert seen[0]["task"]["task_id"] == task.task_id
    assert tr.model_id == "contract-test"
