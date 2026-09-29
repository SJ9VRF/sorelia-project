from pathlib import Path
import json
import matplotlib.pyplot as plt

ROOT = Path(__file__).parents[1]
rows = json.loads((ROOT / 'artifacts/comparison.json').read_text())
final = {m: [r for r in rows if r['mode']==m][-1] for m in sorted({r['mode'] for r in rows})}

modes = list(final)
succ = [final[m]['task_success_rate'] for m in modes]
fails = [final[m]['failures_per_task'] for m in modes]

plt.figure(figsize=(8,4.5))
plt.bar(modes, succ)
plt.ylabel('Task success rate')
plt.ylim(0,1.05)
plt.title('Local sandbox smoke test — equal cumulative training budget')
plt.tight_layout()
plt.savefig(ROOT/'artifacts/smoke_success.png', dpi=180)
plt.close()

plt.figure(figsize=(8,4.5))
plt.bar(modes, fails)
plt.ylabel('Failure events per eval task')
plt.title('Local sandbox smoke test — lower is better')
plt.tight_layout()
plt.savefig(ROOT/'artifacts/smoke_failures.png', dpi=180)
plt.close()

lines = ['# Smoke-test results', '',
         'These numbers validate the research harness only. They are **not** evidence about real browser/desktop agents.', '',
         '| Curriculum | Final task success | Failure events / task | Cumulative training tasks |',
         '|---|---:|---:|---:|']
for m in modes:
    r=final[m]
    lines.append(f"| {m} | {r['task_success_rate']:.3f} | {r['failures_per_task']:.3f} | {r['training_tasks_cumulative']} |")
lines += ['', '## Interpretation', '',
          'The local loop trains and re-evaluates correctly under equal data budgets. In this single-seed toy environment, the adaptive SORELIA curriculum reduces failure events relative to the random curriculum, but does not dominate all baselines on final task success. No superiority claim is made from this run.', '',
          'Paper claims require real computer-use environments, multiple seeds, multiple trials per task, held-out environment families, confidence intervals, human calibration, and the full negative-control/ablation matrix.', '']
(ROOT/'docs/RESULTS_SMOKE.md').write_text('\n'.join(lines), encoding='utf-8')
