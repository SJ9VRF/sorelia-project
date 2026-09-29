from __future__ import annotations
import argparse, json
from sorelia.experiments_multiseed import run_multiseed

p = argparse.ArgumentParser()
p.add_argument('--config', default='configs/paper_smoke.yaml')
p.add_argument('--out', default='artifacts/paper_smoke/multiseed.json')
a = p.parse_args()
res = run_multiseed(a.config, a.out)
print(json.dumps(res['summary'], indent=2, sort_keys=True))
