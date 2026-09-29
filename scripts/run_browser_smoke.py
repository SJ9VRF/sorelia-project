from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
from sorelia.agents.policy import PolicyAgent
from sorelia.adapters.playwright_env import PlaywrightEnvironmentAdapter
from sorelia.benchmarks.tasks import make_tasks
from sorelia.infra.rollout import run_suite
from sorelia.evals.metrics import compute_metrics


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='artifacts/browser_smoke.json'); ap.add_argument('--tasks', type=int, default=12); ap.add_argument('--seed', type=int, default=73)
    a=ap.parse_args(); chromium=shutil.which('chromium')
    if not chromium: raise SystemExit('system chromium not found')
    tasks=make_tasks(a.tasks, seed=a.seed, prefix='browser-real')
    agent=PolicyAgent(seed=a.seed, version='browser-smoke-v0')
    factory=lambda task: PlaywrightEnvironmentAdapter(task, executable_path=chromium)
    trajectories=run_suite(agent,tasks,allow_recovery=True,env_factory=factory)
    payload={'evidence_tier':'local_real_browser_fixture','browser':chromium,'tasks':a.tasks,'seed':a.seed,'metrics':compute_metrics(trajectories),'trajectories':[t.to_dict() for t in trajectories]}
    p=Path(a.out); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps(payload['metrics'],indent=2,sort_keys=True))
if __name__=='__main__': main()
