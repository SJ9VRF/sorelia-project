from sorelia.analysis.statistics import bootstrap_mean_ci, js_divergence

def test_bootstrap_constant():
    x = bootstrap_mean_ci([1,1,1,1], n_boot=100)
    assert x['mean'] == 1.0 and x['ci_low'] == 1.0 and x['ci_high'] == 1.0

def test_js_identity():
    p = {'a': .4, 'b': .6}
    assert abs(js_divergence(p, p)) < 1e-12
