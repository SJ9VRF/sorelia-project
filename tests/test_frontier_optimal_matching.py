import numpy as np
from sorelia.analysis.frontier import cluster_frontier_transition

def c(cid, centroid, risk_scale=1.0):
    return {cid: {"size": 10, "severity": .5, "recoverability": .5, "family": "browser", "failure_type": "grounding", "centroid": centroid}}

def test_optimal_matching_preserves_global_identity():
    before = {}
    before.update(c(0, [1.,0.]))
    before.update(c(1, [.8,.6]))
    after = {}
    after.update(c(0, [.98,.2]))
    after.update(c(1, [.65,.76]))
    r = cluster_frontier_transition(before, after, iteration=1, match_threshold=.5)
    pairs = {(x["before_cluster"], x["after_cluster"]) for x in r["mechanisms"] if x["before_cluster"] is not None and x["after_cluster"] is not None}
    assert len(pairs) == 2
