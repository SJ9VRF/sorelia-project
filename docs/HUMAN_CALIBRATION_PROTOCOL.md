# Human calibration protocol

SORELIA's cross-round mechanism identity is automatic, but the paper-scale study must test whether those identity links agree with human judgments. The repository therefore exports a **blank** annotation packet; it does not fabricate human labels.

## Unit of annotation

Each row is a proposed `before_cluster -> after_cluster` mechanism identity match. Annotators receive the stable ID, cluster IDs, dominant family/type, model similarity, assignment margin, and a notes field. In the real study, representative failure examples and state/action traces should also be rendered in the annotation UI.

Allowed labels:

- `same` - the two clusters represent the same underlying failure mechanism;
- `different` - they do not;
- `uncertain` - evidence is insufficient.

Annotators should not see each other's labels. For the headline calibration set, they should also be blinded to the model's `ambiguous` flag where practical; the machine diagnostics can be joined after labeling.

## Commands

```bash
sorelia calibration-packet --frontier artifacts/run/frontier_i2.json --out annotations/a.jsonl
# Duplicate the blank packet for a second independent annotator.
sorelia calibration-score --annotator-a annotations/a.jsonl --annotator-b annotations/b.jsonl
```

The scorer reports raw agreement, Cohen's kappa, and matcher-vs-human accuracy/precision/recall on rows labeled `same` or `different`.

## Paper gate

Do not promote automatic matching to a validated scientific measure until:

1. at least two independent annotators label a pre-registered sample across multiple seeds/environments;
2. inter-annotator agreement is reported;
3. the similarity/margin ambiguity threshold is selected on a calibration split, not the final test split;
4. matcher quality is reported on a held-out annotation split;
5. disagreements and uncertain cases are retained rather than silently discarded.

The local utilities are executable infrastructure only. **No human-calibration result is claimed in v0.9.**
