from sorelia.analysis.frontier import cluster_frontier_transition

def _c(v, family='browser', typ='grounding'):
    return {'size':5,'severity':.5,'recoverability':.5,'family':family,'failure_type':typ,
            'centroid':v,'failure_ids':['x'],'difficulty':.5,'step_fraction':.5}

def test_matching_calibration_is_reported():
    before={0:_c([1.,0.,0.]),1:_c([0.,1.,0.], 'docs','planning')}
    after={7:_c([.99,.01,0.]),8:_c([.01,.99,0.], 'docs','planning')}
    r=cluster_frontier_transition(before,after,iteration=1,match_threshold=.5)
    cal=r['matching_calibration']
    assert cal['matched']==2
    assert cal['mean_similarity'] > .9
    assert cal['ambiguous_rate'] == 0.0
    assert all('match_margin' in m for m in r['mechanisms'] if m['after_cluster'] is not None and m['before_cluster'] is not None)
