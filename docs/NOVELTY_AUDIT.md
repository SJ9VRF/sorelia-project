# SORELIA Novelty Audit — September 2026

Author: **Aura Yavary**

## Bottom line

The old framing — "turn agent failures into synthetic training data" — is **not sufficiently novel by itself** in 2026. Several strong prior works already occupy that space. SORELIA is therefore framed around a stricter object: **the moving failure frontier** and how training budget should follow its longitudinal dynamics.

This audit does **not** claim that no unpublished or unindexed work overlaps. It records the closest public work found in the search and defines the narrower contribution we can defend.

## Closest prior work

| Work | What it already does | Overlap with old idea | What SORELIA must add to be distinct |
|---|---|---:|---|
| WebRL, ICLR 2025 | self-evolving online curriculum; generates tasks from unsuccessful attempts; RL for web agents | Very high | longitudinal failure-frontier dynamics; explicit extinction/emergence; risk displacement tests; transition-aware budget allocation |
| UI-Genie, NeurIPS 2025 | iterative self-improvement for GUI agents; reward-guided exploration and outcome verification | High | optimize changing failure mechanisms rather than solvable-task expansion/reward-guided exploration |
| Teaching Text Agents to Learn Sequential Decision Making from Failure, ACL 2025 | uses failed actions and perturbations of unsuccessful trajectories | Medium-high | multimodal interactive frontier tracking across iterations and risk-aware curriculum allocation |
| Training a Generally Curious Agent, ICML 2025 | curriculum prioritizes trajectories with high learning potential | Medium | failure-specific longitudinal risk dynamics and explicit new-failure displacement measurement |
| Learning from Failure: Inference-Time Self-Improvement for Computer-Use Agents, 2026 | diagnoses failed computer-use trajectories and creates inference-time code patches | High in motivation, different intervention | SORELIA is train-time curriculum optimization, not inference-time patching; must show frontier movement under policy updates |
| UI-Mem, 2026 | failure diagnosis and correction guidelines in experience memory for mobile GUI agents | Medium | no memory-only framing; focus on cross-iteration failure-risk allocation and verified post-training |

## Public sources

- WebRL: https://proceedings.iclr.cc/paper_files/paper/2025/hash/c66e1fcc9691aae706250638f36f681b-Abstract-Conference.html
- UI-Genie: https://proceedings.nips.cc/paper_files/paper/2025/hash/dd1577afd396928ed64216f3f1fd5556-Abstract-Conference.html
- Teaching Text Agents to Learn Sequential Decision Making from Failure: https://aclanthology.org/2025.acl-long.1526/
- Training a Generally Curious Agent: https://proceedings.mlr.press/v267/tajwar25a.html
- Learning from Failure: Inference-Time Self-Improvement for Computer-Use Agents: https://www.alphaxiv.org/abs/2606.31270
- UI-Mem: https://ui-mem.github.io/

## Defensible SORELIA contribution

SORELIA treats an agent's failure distribution as a **dynamic frontier**, not a static source of training examples.

For each stable failure mechanism across adjacent policy versions, it asks:

1. Did the mechanism become **extinct**?
2. Is it **contracting**?
3. Does it **persist** despite targeted training?
4. Is it **expanding**?
5. Did a previously unseen mechanism **emerge** after the update?

The curriculum then spends a fixed verified-data budget according to these transition states and measured risk, while reserving exploration budget for failure modes that have not yet been characterized.

## Novelty claims we should NOT make

Do not write any of the following without substantially broader literature verification and empirical evidence:

- "first system to learn from failures"
- "first self-improving computer-use agent"
- "first failure-driven curriculum"
- "first agent to generate synthetic tasks from unsuccessful trajectories"
- "first closed-loop agent post-training system"

Those claims conflict with public prior work or are too broad to defend.

## Claims worth testing

The strongest paper claim is comparative and falsifiable:

> Under an equal verified-data budget, transition-aware allocation over the moving failure frontier reduces persistent/expanding failure risk more efficiently than random, difficulty-only, failure-frequency, and static failure-priority curricula, while producing less compensating emergent risk on held-out environments.

A second strong claim would be:

> Aggregate success can improve while reliability worsens because error mass migrates into newly emergent mechanisms; frontier-aware evaluation detects this displacement and can change the next curriculum accordingly.

If the experiments do not support these claims, the paper should report the null result rather than relabel a generic success gain as novelty.
