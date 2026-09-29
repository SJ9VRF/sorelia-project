from sorelia.curriculum.bandit import UCBAllocator

def test_bandit_budget_exact():
    s = {0:{'severity':.2}, 1:{'severity':.9}, 2:{'severity':.4}}
    b = UCBAllocator()
    a = b.allocate(s, 17, .2)
    assert sum(a.values()) == 17
    assert set(a) == set(s)
