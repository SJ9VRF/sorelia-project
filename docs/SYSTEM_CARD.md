# SORELIA system card

## System

**SORELIA — Tracking and Training the Moving Failure Frontier of Interactive Agents**  
Author: **Aura Yavary**

## Intended use

Research on longitudinal agent reliability: discovering failure mechanisms, tracking how they change across policy updates, allocating verified training budget, and measuring risk displacement.

## Components

- provider-agnostic observation-aware agent interface;
- deterministic sandbox and isolated Chromium/Playwright environment;
- trajectory/failure/recovery schema;
- failure clustering and optimal cross-round mechanism matching;
- fixed-budget curriculum allocators and negative controls;
- deterministic/state-based verification;
- SFT/preference/correction data builders;
- repeated-trial/multiseed evaluation and paired statistics;
- contamination, provenance, evidence, and usage-accounting gates.

## Out-of-scope claims

The release does not establish SOTA performance, production safety, frontier-model post-training gains, or validated performance on uncontrolled external websites.

## Safety boundary

High-risk actions should be mocked in isolated environments. Provider/network/parser failures are infrastructure failures, not scientific agent-failure observations.

## Evidence boundary

Committed numerical results are engineering smoke evidence. See `docs/EVIDENCE_TIERS.md`, `docs/TRUTH_AUDIT.md`, and `docs/PAPER_READINESS.md`.
