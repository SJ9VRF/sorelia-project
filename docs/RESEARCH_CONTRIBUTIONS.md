# Intended research contributions — v0.7.0

SORELIA is designed around contributions that are independently falsifiable.

1. **Longitudinal mechanism identity.** Failure clusters are discovered per round but matched across policy versions using structured centroid signatures and stable mechanism IDs rather than assuming cluster IDs or coarse taxonomies are stable.
2. **Failure-frontier topology.** The system measures extinction, contraction, persistence, expansion, emergence, and split/merge events across updates.
3. **Risk-displacement evaluation.** An update is not treated as a clean reliability gain if removed risk is offset by newly introduced or expanding risk.
4. **Transition-aware allocation.** A fixed verified-data budget follows the moving frontier, with explicit exploration rather than static failure-frequency sampling.
5. **Counterfactual verified curricula.** Generated tasks preserve failure mechanism while changing surface factors and enter training only after executable validation and duplicate filtering.
6. **Auditable closed-loop lineage.** Stable mechanism IDs, source failures/clusters, generation iteration, mutation signature and verifier version make the evaluation-to-training loop inspectable.

The strongest publishable claim is not that failure-driven training works. It is that **failure-transition information adds measurable value beyond static failure-conditioned curricula under equal budgets, or exposes risk displacement hidden by aggregate success.** If neither effect appears on real agents, the central hypothesis is not supported.
