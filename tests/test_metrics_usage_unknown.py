from sorelia.evals.metrics import compute_metrics
from sorelia.schema import Trajectory


def tr(*, known=False, success=True):
    return Trajectory(
        trajectory_id='x', task_id='t', task_family='browser', model_id='m', model_version='v', seed=1,
        initial_state={}, success=success, partial_success=float(success), grader_results={}, num_steps=1,
        tokens=10 if known else 0, input_tokens=7 if known else 0, output_tokens=3 if known else 0,
        usage_known=known, model_latency_ms=12 if known else 0, monetary_cost=.5 if known else 0,
        cost_known=known,
    )


def test_unknown_cost_is_not_reported_as_zero():
    m = compute_metrics([tr(known=False)])
    assert m['mean_cost'] is None
    assert m['cost_per_success'] is None
    assert m['mean_input_tokens'] is None
    assert m['usage_coverage'] == 0.0
    assert m['cost_coverage'] == 0.0


def test_measured_cost_and_usage_are_aggregated_only_when_known():
    m = compute_metrics([tr(known=True), tr(known=False)])
    assert m['mean_cost'] == .5
    assert m['mean_input_tokens'] == 7
    assert m['mean_output_tokens'] == 3
    assert m['usage_coverage'] == .5
    assert m['cost_coverage'] == .5
