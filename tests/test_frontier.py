from sorelia.analysis.frontier import frontier_transition
from sorelia.schema import Trajectory, FailureEvent


def tr(task_id, family, failure_type=None, severity=.8, recoverability=.2):
    t = Trajectory(task_id, task_id, family, "m", "v", 0, {})
    t.num_steps = 4
    if failure_type:
        t.failure_events.append(FailureEvent(1, failure_type, "x", severity, recoverability, {}, "A", {}, {}))
    return t


def test_frontier_tracks_extinction_and_emergence():
    before = [tr("a", "browser", "grounding"), tr("b", "browser", "grounding")]
    after = [tr("a", "browser", None), tr("b", "browser", "verification")]
    r = frontier_transition(before, after)
    statuses = {(x["family"], x["failure_type"]): x["status"] for x in r["mechanisms"]}
    assert statuses[("browser", "grounding")] == "extinct"
    assert statuses[("browser", "verification")] == "emergent"
