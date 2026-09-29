from sorelia.analysis.frontier import cluster_frontier_transition


def c(size, fam, typ, centroid, sev=.8, rec=.3, stable=None):
    x = {"size": size, "family": fam, "failure_type": typ, "centroid": centroid,
         "severity": sev, "recoverability": rec}
    if stable: x["stable_id"] = stable
    return x


def test_cluster_frontier_inherits_identity_and_detects_emergence():
    before = {0: c(10, "browser", "grounding", [1,0,0], stable="m0")}
    after = {3: c(5, "browser", "grounding", [0.99,.01,0]),
             4: c(3, "browser", "safety", [0,0,1])}
    r = cluster_frontier_transition(before, after, iteration=2, match_threshold=.75)
    assert r["annotated_after"][3]["stable_id"] == "m0"
    assert r["status_by_cluster"]["4"] == "emergent"
    assert r["risk_introduced"] > 0


def test_cluster_frontier_reports_split_topology():
    before = {0: c(10, "browser", "grounding", [1,0,0], stable="m0")}
    after = {1: c(5, "browser", "grounding", [.99,.01,0]),
             2: c(5, "browser", "grounding", [.98,.02,0])}
    r = cluster_frontier_transition(before, after, iteration=2, match_threshold=.75, event_threshold=.75)
    assert any(e["event"] == "split" for e in r["topology_events"])
