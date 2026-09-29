from pathlib import Path
import re, sys, tomllib
ROOT=Path(__file__).resolve().parents[1]
errors=[]
version=tomllib.loads((ROOT/'pyproject.toml').read_text())['project']['version']
required=[
 'README.md','LICENSE','CITATION.cff','CONTRIBUTING.md','SECURITY.md','CODE_OF_CONDUCT.md',
 'SUBMISSION_INDEX.md','docs/BENCHMARK_CARD.md','docs/DATA_CARD.md','docs/SYSTEM_CARD.md','docs/MODEL_CARD.md',
 'docs/EXPERIMENT_REGISTRY.md','docs/EXPERIMENT_JOURNAL.md','docs/FAILED_EXPERIMENTS.md','docs/UNEXPECTED_FINDINGS.md','docs/DECISION_LOG.md','docs/RAW_ARTIFACT_INDEX.md','docs/REVIEWER_REPRODUCTION.md','docs/CURRENT_RESULTS.md','docs/TRACEABILITY_MATRIX.md','docs/EVIDENCE_LEDGER.json','docs/RESEARCH_THREADS.md',
 'paper/main.pdf','website/index.html','website/evidence.html','website/traceability.html','website/demo.html','website/assets/sorelia-demo.mp4',
 'Dockerfile','.devcontainer/devcontainer.json','.github/workflows/ci.yml']
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f'missing required file: {rel}')
# version consistency in canonical public files
for rel in ['pyproject.toml','src/sorelia/__init__.py','CITATION.cff','README.md','website/index.html']:
    txt=(ROOT/rel).read_text(errors='ignore')
    if version not in txt: errors.append(f'version {version} absent from {rel}')
# placeholders/publicly embarrassing stubs
bad=re.compile(r'(?i)(TODO|FIXME|TBD|your-url|example\.com|github\.com/[^\s)]*USERNAME)')
for rel in ['README.md','SUBMISSION_INDEX.md','website/index.html','docs/EXECUTIVE_REVIEW.md','docs/CURRENT_RESULTS.md']:
    txt=(ROOT/rel).read_text(errors='ignore')
    if bad.search(txt): errors.append(f'placeholder-like text in {rel}')
# local markdown links
for p in list(ROOT.glob('*.md'))+list((ROOT/'docs').glob('*.md')):
    txt=p.read_text(errors='ignore')
    for u in re.findall(r'\[[^\]]+\]\(([^)]+)\)',txt):
        u=u.split('#')[0]
        if not u or '://' in u or u.startswith('mailto:'): continue
        if not (p.parent/u).resolve().exists(): errors.append(f'broken local link: {p.relative_to(ROOT)} -> {u}')
# public assets non-empty
for rel in ['paper/main.pdf','website/assets/sorelia-demo.mp4']:
    p=ROOT/rel
    if p.exists() and p.stat().st_size < 1000: errors.append(f'suspiciously small artifact: {rel}')
print(f'public release version: {version}')
print(f'errors: {len(errors)}')
for e in errors: print('ERROR:',e)
sys.exit(1 if errors else 0)
