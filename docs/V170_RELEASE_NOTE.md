# SORELIA v1.7.0 — Traceability Layer

v1.7.0 turns the Evidence Layer into an auditable research graph. Four retained research threads connect hypothesis → executed experiment → failed assumption → decision → raw artifact → implementation/config → current conclusion. A machine-readable evidence ledger stores SHA-256 hashes for raw evidence and source/config files. Historical Git boundaries remain explicit: commits before the retained v1.5.0 baseline are not reconstructed.

The release adds `docs/TRACEABILITY_MATRIX.md`, `docs/EVIDENCE_LEDGER.json`, `docs/RESEARCH_THREADS.md`, `website/traceability.html`, `scripts/validate_traceability.py`, and traceability contract tests.
