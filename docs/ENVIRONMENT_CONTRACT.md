# Environment and model contracts

SORELIA separates the research loop from a specific browser or model provider.

An environment must implement `reset`, `observe`, `expected_state`, `step`, `verify`, and `rollback_local`. Core grading should derive from environment state whenever possible. A production browser implementation should create an isolated context per trial, restore a deterministic task fixture, capture screenshot/DOM/accessibility observations, execute typed actions through a safety gate, store pre/post state, and use explicit success predicates.

An agent must expose a version and `act(task, step, deterministic=False)`. Production adapters can wrap a VLM, computer-use model, or local policy. Training code should remain separate from inference adapters so SFT, preference optimization, and RL can be compared without changing evaluation semantics.

The included `InteractiveSandbox` is the executable reference implementation of these contracts. `adapters/playwright_env.py` documents the production-facing replacement boundary; it is not counted as an executed browser experiment.
