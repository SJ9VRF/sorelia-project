from sorelia.analysis.statistics import paired_bootstrap_delta, paired_permutation_test

def test_paired_statistics_direction():
    a=[1,1,1,1,1,1,1,1]
    b=[0,0,0,0,0,0,0,0]
    ci=paired_bootstrap_delta(a,b,seed=1,n_boot=1000)
    pt=paired_permutation_test(a,b,seed=1,n_perm=4000)
    assert ci["mean_delta"] == 1.0 and ci["ci_low"] > 0
    assert pt["p_value"] < .05
