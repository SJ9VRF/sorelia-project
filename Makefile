.PHONY: install test smoke compare multiseed compile release-check clean
install:
	pip install -e .
test:
	pytest -q
compile:
	python -m compileall -q src
smoke:
	sorelia run --config configs/smoke.yaml --out artifacts/smoke
compare:
	sorelia compare --config configs/smoke.yaml --out artifacts/comparison.json
multiseed:
	sorelia multiseed --config configs/paper_smoke.yaml --out artifacts/paper_smoke/multiseed.json
release-check: test compile
	PYTHONPATH=src python scripts/run_multiseed.py --config configs/paper_smoke.yaml --out artifacts/paper_smoke/multiseed.json
clean:
	rm -rf artifacts/smoke artifacts/comparison.json artifacts/paper_smoke .pytest_cache

.PHONY: audit reproduce-release paper-rehearsal

audit:
	PYTHONPATH=src python -m sorelia.cli audit --root .

reproduce-release:
	bash scripts/reproduce_release.sh

paper-rehearsal:
	bash scripts/rehearse_paper_protocol.sh

.PHONY: reviewer-demo
reviewer-demo:
	bash scripts/reviewer_demo.sh

.PHONY: public-audit release-candidate
public-audit:
	PYTHONPATH=src python scripts/validate_public_release.py
release-candidate: test compile audit public-audit

