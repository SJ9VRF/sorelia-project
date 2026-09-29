# Related work positioning

SORELIA is intentionally positioned **after** several strong self-improvement and failure-learning systems, not as if they did not exist.

- **WebRL (ICLR 2025)** generates new web tasks from unsuccessful attempts inside a self-evolving online curriculum. This makes generic failure-conditioned task generation non-novel.
- **UI-Genie (NeurIPS 2025)** iteratively improves GUI agents using reward-guided exploration, outcome verification and synthetic trajectory generation.
- **Teaching Text Agents to Learn Sequential Decision Making from Failure (ACL 2025)** uses failed actions and perturbations of unsuccessful trajectories for learning.
- **Training a Generally Curious Agent (ICML 2025)** prioritizes interaction data with high learning potential, showing that adaptive sampling itself is also established.
- **Learning from Failure: Inference-Time Self-Improvement for Computer-Use Agents (2026)** turns failed computer-use trajectories into diagnosis and code patches without retraining.
- **UI-Mem (2026)** uses failure diagnosis to create correction guidance in a self-evolving experience memory.

SORELIA's target is narrower: **longitudinal failure-frontier dynamics after policy updates** and **transition-aware fixed-budget curriculum allocation**. The central evaluation asks whether risk is removed, persists, expands, or is displaced into new mechanisms.

See `NOVELTY_AUDIT.md` for the full overlap matrix and links.
