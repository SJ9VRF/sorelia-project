# When an Agent Gets Better, Where Do Its Failures Go?

*Aura Yavary*

A single success rate can hide the most important thing that happened after post-training.

Suppose an interactive agent improves from 71% to 79% task success. That looks good. But imagine grounding failures collapse while a new class of unsafe irreversible actions appears. Did the agent become more reliable, or did reliability risk move somewhere harder to see?

That is the question behind **SORELIA**.

Most self-improvement loops naturally focus on collecting failures, generating more data, and updating the policy. SORELIA adds a longitudinal view: it tries to preserve the identity of failure mechanisms across model versions and asks what happened to each one after training. A mechanism can become extinct, contract, persist, expand, or newly emerge. It can also split into narrower failures or merge with others.

The resulting object is a **moving failure frontier** rather than a single leaderboard number.

This changes how the next training budget is allocated. SORELIA gives more attention to persistent, expanding, and emergent risk while keeping an exploration reserve. More importantly, it measures both risk removed and risk introduced. A model update that fixes yesterday's failures while creating compensating new ones should not be counted as an unqualified reliability win.

The repository is deliberately built to make this hypothesis falsifiable. Baselines receive the same verified-data budget. The harness includes static failure priority, shuffled labels, random clusters, repeated trials, shifted stress evaluation, leakage gates, and paired statistical tests. Null and adverse outcomes are retained.

The current public results are engineering smoke tests, not frontier-model claims. One retained local update is useful precisely because it illustrates the measurement problem: aggregate task success stayed at 90% while the measured risk-displacement ratio rose above 1, meaning introduced frontier risk exceeded removed frontier risk in that toy setting. The point is not that this number generalizes. The point is that an aggregate success score alone would not have exposed it.

The next scientific test is straightforward but expensive: run the same protocol with trainable computer-use models, independently authored tasks, held-out sites and applications, enough seeds and repeated trials, and independently calibrated mechanism identities. If moving-frontier information does not outperform strong static allocation under those conditions, the central SORELIA hypothesis should be rejected or narrowed.

That is the standard the project is designed around: not a story that always wins, but a system capable of showing when the story is wrong.
