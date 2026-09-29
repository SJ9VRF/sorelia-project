# Negative controls

A failure-conditioned curriculum is only meaningful if the detected failure semantics matter. v0.9 makes two previously planned controls executable.

## Shuffled failure labels

After clustering, dominant failure labels are permuted across clusters before targeted generation. Cluster sizes and other statistics remain available, but the semantic link from observed mechanism to generated task is corrupted.

If this control performs as well as or better than full SORELIA on real-agent studies, the claim that targeted failure semantics drive the benefit is weakened.

## Random cluster assignment

Observed failure points are randomly reassigned among discovered cluster IDs before cluster summaries and curriculum generation are built.

If this control matches full SORELIA, the discovered cluster structure may not be carrying causal signal.

## Interpretation

These controls are intentionally allowed to win. In the v0.9 local toy smoke, some negative-control/static variants outperform full SORELIA on some metrics. That result is retained and is one reason no superiority claim is made from the sandbox.
