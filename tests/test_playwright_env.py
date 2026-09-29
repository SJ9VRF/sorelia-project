import shutil
import pytest
from sorelia.adapters.playwright_env import PlaywrightEnvironmentAdapter
from sorelia.benchmarks.tasks import make_tasks
from sorelia.features import correct_action

pytestmark = pytest.mark.skipif(shutil.which("chromium") is None, reason="system chromium unavailable")

def test_real_browser_fixture_state_based_grading():
    task = make_tasks(1, seed=31, prefix="browser")[0]
    task.horizon = 3
    env = PlaywrightEnvironmentAdapter(task, executable_path=shutil.which("chromium"))
    try:
        obs = env.reset()
        assert len(obs["visible_actions"]) == 4
        while env._completed < task.horizon:
            action = correct_action(task, env._step)
            obs, done, info = env.step(action)
            assert info["correct"]
            if done:
                break
        grades = env.verify()
        assert grades["task_success"] == 1.0
        assert obs["completed"] == task.horizon
    finally:
        env.close()
