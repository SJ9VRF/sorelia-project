from pathlib import Path
import json
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[1]
data = json.loads((root/'artifacts/paper_smoke/multiseed.json').read_text())
summary = data['summary']
modes = list(summary)
means = [summary[m]['task_success_rate']['mean'] for m in modes]
low = [means[i]-summary[m]['task_success_rate']['ci_low'] for i,m in enumerate(modes)]
high = [summary[m]['task_success_rate']['ci_high']-means[i] for i,m in enumerate(modes)]
fig, ax = plt.subplots(figsize=(8,4.5))
ax.bar(modes, means, yerr=[low,high], capsize=4)
ax.set_ylim(0.85, 1.01)
ax.set_ylabel('Task success rate')
ax.set_title('Five-seed engineering smoke test (95% bootstrap CI)')
fig.tight_layout()
fig.savefig(root/'artifacts/paper_smoke/multiseed_success.png', dpi=180)
plt.close(fig)

lines = ['# Multi-seed engineering smoke test', '',
         '> These results validate the experimental harness. They are **not** evidence for real computer-use performance.', '',
         f"Seeds: {', '.join(map(str,data['seeds']))}. Final iteration: {data['final_iteration']}.", '',
         '| Curriculum | Success mean | 95% bootstrap CI | Failures/task | Catastrophic rate |',
         '|---|---:|---:|---:|---:|']
for m in modes:
    s=summary[m]
    x=s['task_success_rate']; f=s['failures_per_task']; c=s['catastrophic_action_rate']
    lines.append(f"| {m} | {x['mean']:.3f} | [{x['ci_low']:.3f}, {x['ci_high']:.3f}] | {f['mean']:.3f} | {c['mean']:.3f} |")
lines += ['', 'Interpretation: in this deliberately small synthetic state-machine environment, SORELIA ties random on mean final task success and does not dominate every metric. The result is useful because the harness exposes null/mixed outcomes instead of manufacturing a positive paper claim. Real claims require the paper-scale browser experiments described in `docs/EXPERIMENTS.md`.']
(root/'docs/RESULTS_MULTISEED_SMOKE.md').write_text('\n'.join(lines)+'\n')
