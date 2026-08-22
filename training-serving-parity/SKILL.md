---
name: training-serving-parity
description: Hunt the gap between the features a model was trained on and the features it is actually served — two implementations of one computation, a value that is complete offline and partial online, preprocessing shipped separately from the model, and the silent default that fills in a failed feature so the model answers confidently on a vector it never saw. Use whenever a model is deployed, whenever a feature pipeline exists in more than one place, and whenever offline and online results disagree. Trigger on "training/serving skew", "it works offline but not in production", "the model degraded but nothing changed", "feature store", "point-in-time correctness", "we compute this in Spark and in Go", "backfill", "the preprocessing lives in the API", "feature drift", "model monitoring", "why is production accuracy lower", or a feature computed once for training and again at inference. The ML instance of parser-differential-hunting: same input, two meanings, and the path that decides is not the path that acts.
---

# Training / Serving Parity

A model is a function fitted to one feature distribution and then run against
whatever the serving path produces. When those two differ, nothing errors. The
model returns a confident, well-formed, wrong prediction, the offline metrics
stay excellent, and the gap belongs to no team: the training pipeline is
correct, the serving pipeline is correct, and the composition is broken.

The invariant, and it is the whole skill:

> **`features_train(x, t) == features_serve(x, t)`** — for the same entity at
> the same moment, both paths must produce the same vector. Not similar. The
> same.

This is `parser-differential-hunting` with different vocabulary. There too, two
implementations read one input and disagree; there too, each is locally
reasonable; there too, the finding is that the component which *decides* is not
the component which *acts*. Here the deciding component is the training run
that fixed the model's weights, and the acting component is the request path
months later.

Composes with the library:

- **parser-differential-hunting** — the same structure, the same harness, the
  same fix ladder; read it for the general method
- **data-leakage-hunting** — the sibling failure at the other end: that skill
  catches the offline number being too good, this one catches the online
  outcome being worse
- **honest-degradation** — the silent default in Part 4 is its archetype
- **training-run-provenance** — the model and its transform are one versioned
  artifact, not two
- **model-evaluation-discipline** — the offline evaluation cannot see any of
  this; Part 5 says what can
- **forensic-logging-design** — the serving feature vector is the telemetry
  that makes all of this diagnosable

---

## Part 1 — The four skew families

1. **Implementation skew.** The feature is computed twice, in two languages, by
   two teams, months apart — Spark SQL or pandas for training, Go or Java in
   the request path. Every one of these is a real, recurring divergence:
   null handling (`mean()` skipping nulls offline, treating them as zero
   online), rounding and float width, string normalization and case folding,
   timezone and date-boundary handling, unseen-category encoding, one-hot
   column *order*, clipping bounds, and the default that each side chose
   independently for a missing value.
2. **Point-in-time skew.** Training used a value as it looks in the warehouse —
   complete, settled, backfilled. Serving sees it partial. A daily aggregate is
   a full day offline and six hours online; a counter is final offline and
   still incrementing online; a status field is the corrected version offline
   and the provisional one online. The training row is not wrong, and it is not
   reproducible at request time — which is the definition of this family.
3. **Pipeline-state skew.** Vocabularies, embedding tables, scaler statistics,
   category mappings, and bucket boundaries shipped *separately* from the
   model. The model is redeployed and the transform is not, or the feature
   store is backfilled with a newer transform than the one the model was fitted
   under. Everything versions independently until one of them moves.
4. **Distribution skew.** The serving population is not the training
   population — a new integration, a new country, a new client that dominates
   traffic, a seasonal shift. And the feedback loop: the model changes which
   requests it later receives, so the drift is partly self-inflicted.

Families 1–3 are defects and are fixable by construction. Family 4 is a fact
about the world and is managed by monitoring and retraining. Separate them
before proposing anything, because the fixes have nothing in common.

## Part 2 — Fix by construction, ranked

The point fix ("we corrected the null handling in the Go service") loses for
the same reason it loses in parser differentials: the next feature reintroduces
it. Rank the remediation:

1. **One implementation, called by both paths.** The transform is a single
   artifact — one library, one function, one version — imported by the training
   job and by the serving path. This deletes families 1 and 3 outright.
2. **Log-and-train.** Compute the feature vector once, *at serving time*, log
   it, and train on the logged vectors. Serving becomes the source of truth and
   implementation skew becomes structurally impossible. It costs a bootstrap
   problem for a brand-new model and is worth it from the second model onward.
3. **Ship preprocessing with the model as one atomic artifact.** The weights
   and their transform are a single versioned unit that cannot be deployed
   independently (`training-run-provenance`). If they can be deployed
   separately, one day they will be.
4. **A feature store with point-in-time correctness** for family 2 — training
   reads values "as of the event", never "as of now", and serving reads the
   same view. If you do not have one, the substitute is to build training rows
   from the *logged* online values.
5. **If two implementations genuinely must exist** (a latency budget the
   training stack cannot meet), then the differential harness of Part 3 is
   mandatory and belongs in CI. Two implementations without a differential test
   is not a tradeoff, it is an unmonitored bug.
6. Only then: drift monitoring, which detects rather than prevents.

## Part 3 — The differential harness

Cheap, offline, and it finds real defects on the first run in most systems.

1. **Take N real serving requests** — sampled from production logs, including
   the ugly ones: missing fields, new categories, extreme values, and the
   slowest 1%.
2. **Replay through both paths** and compare **feature by feature**.
3. **State the tolerance per type, in advance.** Exact equality for categorical,
   integer, boolean and encoded columns. An explicit epsilon for floats — and
   epsilon is a decision to write down, not a default to inherit.
4. **Report per-feature mismatch rates, never an aggregate.** "97% of features
   match" hides that the 3% is the top-importance feature. One broken column out
   of two hundred is a broken model.
5. **Rank mismatches by feature importance.** A skewed feature the model barely
   uses is a cleanup ticket; a skewed top-five feature is an incident.
6. **Freeze a golden set** — those N requests with their expected vectors — and
   run it in CI on every change to either path.

Same discipline as any differential: compare the projection that matters, and
triage each mismatch by whether it reaches the thing that acts.

## Part 4 — The silent default is the failure you will actually hit

A feature service times out. The lookup returns nothing. The code fills in
`0`, or the training-set mean, or an empty embedding — and the model returns a
confident prediction on a vector it was never fitted on. Nothing logs an error.
The latency graph looks fine. This is the single most common way a deployed ML
system degrades, and `honest-degradation` names it exactly: a plausible answer
produced from data that was not there.

What to do:

- **Count and export the default rate per feature.** It is the highest-value
  metric in ML serving and almost nobody emits it. A default rate that moves
  from 0.1% to 8% is an outage, whatever the prediction distribution says.
- **Decide the degraded behavior deliberately, per feature.** Fail the request,
  abstain, or fall back to a simpler model that does not use that feature —
  each is defensible. Silently imputing and answering anyway is not.
- **Make abstention a first-class output**, and measure coverage alongside
  accuracy (`model-evaluation-discipline` Part 2).
- **Log the served feature vector, sampled.** Without it, a wrong prediction
  cannot be reconstructed — you have the input and the output and none of the
  middle. With it, every incident in this skill is diagnosable in minutes.

## Part 5 — Monitor features, not just predictions

The prediction distribution is a lagging and weak signal: it moves late, and it
moves for many reasons. Watch the inputs.

Per feature, alert on: null and default rate, cardinality (new categories
appearing, old ones vanishing), range and quantile shift, and freshness — the
age of the value at the moment it was used. Compare each against the *training*
distribution, which means the training distribution has to be stored as an
artifact alongside the model.

And for the final honest number: **evaluate on logged serving features joined
to real outcomes**, not on a rebuilt offline feature set. That is the only
evaluation that has seen the serving path, and it is the one that would have
caught every family above.

---

## Deliverable

```
## Parity review — <model> <version>
Feature paths: training <impl> | serving <impl> | shared code: yes/no
Transform artifact shipped with weights: yes/no
Point-in-time correctness: <how training values are made reproducible online>

### Differential run (N = <n> replayed production requests)
feature | type | tolerance | mismatch rate | importance rank | family

### Silent-default exposure
feature | default value | current default rate | degraded behavior chosen

### Fixes (ranked, structural first)
### Monitoring added: per-feature null/default/cardinality/range/freshness
### Not covered
```

## Anti-patterns

- Two implementations of one feature and no differential test between them.
- Reporting an aggregate match rate instead of per-feature mismatches.
- Comparing floats with an inherited default tolerance nobody chose.
- Deploying the model and its preprocessing as independently versioned things.
- Building training rows from warehouse values that the request path cannot
  reproduce, and calling the gap "drift".
- Imputing a failed feature lookup and answering confidently.
- Not emitting a per-feature default rate, so degradation is invisible until
  someone notices the business metric.
- Monitoring only the prediction distribution.
- Never logging the served feature vector, leaving wrong predictions
  permanently undiagnosable.
- Retraining to fix what is an implementation bug — it hides the skew inside
  new weights and the gap comes back with the next feature.
