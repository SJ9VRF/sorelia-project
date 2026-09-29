from sorelia.experiments import MODES, _make_curriculum

def test_static_priority_baseline_is_real_mode():
    assert 'priority' in MODES
    summary = {0:{'size':4,'severity':.8,'recoverability':.7,'family':'browser','failure_type':'grounding','centroid':[1,0],'difficulty':.6,'step_fraction':.5,'failure_ids':['a']},
               1:{'size':2,'severity':.2,'recoverability':.3,'family':'docs','failure_type':'planning','centroid':[0,1],'difficulty':.4,'step_fraction':.4,'failure_ids':['b']}}
    tasks, alloc = _make_curriculum('priority', summary, 12, 1, 0, .2)
    assert sum(alloc.values()) == 12
    assert len(tasks) == 12
