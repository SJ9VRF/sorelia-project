# SORELIA model / policy card

## What this release contains
SORELIA is primarily an evaluation/post-training research system, not a released frontier model. The repository includes a deterministic/trainable local reference policy plus provider-agnostic interfaces and optional OpenAI Responses / Anthropic Messages adapters.

## Intended use
- exercise the closed-loop research harness
- validate trajectory, failure, recovery, grading, curriculum, and provenance paths
- connect an authorized interactive model backend without changing the evaluation core

## Not intended as
- a production autonomous agent
- evidence that any proprietary model was trained or evaluated in this release
- a safety certification
- a claim of SOTA capability

## Observation boundary
Policies receive an observation-aware decision context: task metadata, current observation, expected state, bounded recent actions/observations, and step metadata.

## Usage accounting
Provider decisions may return measured input/output tokens and model-call latency. Monetary cost is recorded only when an explicit estimator is supplied. Unknown values remain unavailable/null.

## Known limitations
The bundled local policy and isolated browser fixture are engineering references, not representative frontier agents. Paper-scale conclusions require the gates in `docs/PAPER_READINESS.md`.
