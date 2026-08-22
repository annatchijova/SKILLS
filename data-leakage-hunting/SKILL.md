---
name: data-leakage-hunting
description: Hunt the one bug class in machine learning whose symptom is a better score — information from the evaluation set reaching the model through preprocessing, time, groups, duplicates, features derived from the label, or a test set spent on tuning. Use whenever a dataset is split, a pipeline is fitted, a feature is engineered, a benchmark is reported, or a model performs suspiciously well. Trigger on "data leakage", "target leakage", "train/test contamination", "the accuracy is 99%", "too good to be true", "it works offline but not in production", "why did performance drop after deployment", "should I scale before or after the split", "cross-validation", "random split", "one feature dominates", "duplicate rows", "the benchmark may be in the pretraining data", or any metric that jumped with no change in method. Sibling of invariant-hunting: the invariant is that nothing derived from evaluation data may influence the prediction, and this skill hunts every transition where it silently breaks. It does not tune models.
---

# Data Leakage Hunting

Every other defect makes something fail. This one makes everything look
better — which means the normal feedback loop of engineering runs in reverse.
A leak is discovered by celebration, adopted into the pipeline, published in
the README, and found six months later by production.

So the alarm has to be inverted, and it is the first rule of this skill:

> **An unexpectedly good result is a bug report until proven otherwise.**

The invariant being violated is always the same one, and it is worth writing on
the wall:

> **No information derived from the evaluation data may influence anything used
> to produce the prediction.** Established at the split (T0), it must still hold
> at fit time, at feature-construction time, at tuning time, and at the moment
> the number goes in the report (Tn).

That is `invariant-hunting`'s shape exactly: a property established in one place
that has to survive a journey. The difference is that here the violation
*rewards* you, so nobody goes looking.

Composes with the library:

- **invariant-hunting** — the T0→Tn frame; this is its ML instance
- **model-evaluation-discipline** — the number the leak corrupts, and the
  baselines that make a leak visible
- **training-run-provenance** — the split must be an artifact, not a seed
- **discriminating-proof** — the falsification experiments in Part 3
- **honest-degradation** — a leaked metric is the archetype of a plausible,
  confident, wrong answer
- **daubert-defensible-writing** — how to report that every prior number is void

---

## Part 1 — Write the split contract before you model

Most leaks are decided before a single model is trained, by three questions
nobody wrote down. Answer them in the repo, not in your head:

1. **What is the unit of generalization?** The thing the model must work on
   *next*, that it has never seen: a new user, a new patient, a new document, a
   new day, a new hospital. If the unit is a user and you split on rows, the
   evaluation is measuring memorization of users it already knows.
2. **What is the time boundary?** If the data has a time dimension and the
   model will be used to predict forward, then every evaluation row must be
   strictly after every training row. A random split on time-ordered data lets
   the model interpolate a future it will never have.
3. **What defines a group?** Same entity, same session, same source document,
   near-duplicate image, augmented copies of one original, retried request. All
   copies of one group belong on one side of the split.

Then store the split **as data** — the actual ids or indices, hashed and
versioned — not as the seed that generated it. A seed is not a split: change a
library version and the same seed produces a different partition, and every
comparison you made becomes meaningless (`training-run-provenance`).

## Part 2 — The eight families

Name the family before testing. Each has a distinct habitat and a distinct
falsifier.

1. **Preprocessing fitted before the split.** A scaler, imputer, encoder,
   vocabulary, PCA, feature selector, or normalization statistic computed over
   the full dataset. The single most common leak in existence, and it is one
   line of code *order*. The fix is structural: the entire transformation chain
   lives inside a pipeline object that is fitted on the training fold only —
   and inside each fold in cross-validation, not once around it.
2. **Temporal leakage.** A random split on time-series data; a feature whose
   aggregation window extends past the prediction timestamp; a join that
   attaches a value known only later; a feature store queried "as of now"
   instead of "as of the event". Anything computed with `groupby().mean()` over
   the whole table is a candidate.
3. **Group leakage.** The same entity in both splits — patient, user, device,
   session, article, or several images from one photo series. The score
   measures recall of the entity, not generalization to a new one.
4. **Target leakage in a feature.** A column that is a consequence, proxy, or
   encoding of the label: `account_closed_date` for churn, `n_treatments` for
   diagnosis, a field only populated after the outcome, or an id that
   correlates with the class because of the order in which data was collected.
   The tell is a single feature with implausible importance.
5. **Duplicates and near-duplicates across splits.** Web-scraped corpora,
   augmented copies, retried records, boilerplate. Count them; do not assume.
6. **Tuning on the test set.** The slowest leak and the hardest to see: each
   experiment that peeks transfers a few bits of the test set into your choices.
   Threshold selection, early stopping, feature selection, architecture search,
   and "I tried it and it was worse" are all peeks. After a hundred experiments
   the test set is a training signal.
7. **Label-process leakage.** The annotator saw a model prediction; labels were
   derived from a source that is also a feature; two labellers' agreement was
   used to drop the hard examples. The test set is now easier than reality.
8. **Pretraining contamination.** The benchmark exists in the pretrained model's
   corpus. Standard for any public dataset and any foundation model — and it
   makes a public benchmark an upper bound, not a measurement.

## Part 3 — Falsify, do not eyeball

Suspicion is cheap. These experiments are the discriminating kind — each one
predicts a specific result, and the wrong result is the finding
(`discriminating-proof`).

| Experiment | If the leak is absent | If it is present |
|---|---|---|
| **Shuffle the labels**, retrain | score falls to the baseline | above chance ⇒ leakage or a pipeline bug, with no exceptions |
| **Re-split by group** instead of by row | score changes little | large drop ⇒ group leakage |
| **Re-split by time**, train past → test future | score changes little | large drop ⇒ temporal leakage |
| **Drop the dominant feature** | score degrades gracefully | collapse ⇒ that feature carries the label |
| **Hash / near-dup match across splits** | near-zero overlap | any overlap is a defect, quantified |
| **Train on 10% of the data** | clearly worse | as good ⇒ the task is being solved by something other than learning |
| **Evaluate on a freshly collected period** | within the interval | drop ⇒ the offline set no longer represents reality |

The label shuffle deserves its own line, because it is the negative control this
whole field is missing: **a model trained on randomized labels must not beat the
baseline.** If it does, stop everything — no result from that pipeline means
anything until it is explained.

Run these before you report a good number, not after someone doubts it.

## Part 4 — When you find one, the numbers are void

This is where the reporting discipline matters, because the temptation is to
fix the leak, rerun, and quietly replace the number.

- **Every metric produced by the leaking pipeline is void, not adjusted.** They
  do not get corrected downward; they get withdrawn. Any decision made on them
  (this architecture beat that one, this feature helped) is unsupported and has
  to be re-run.
- **Say it explicitly** wherever the old number lives: README, dashboard,
  paper, ticket, slide. `claim-provenance-discipline` — a number that traveled
  keeps traveling until someone stops it by name.
- **Fix it structurally.** "We removed the ID column" is a point fix for one
  instance. The class fix is a pipeline that *cannot* express the leak: the
  transform chain fitted inside the fold, splits materialized as versioned
  artifacts, a feature store with point-in-time correctness, and a CI check that
  fails on cross-split id overlap.
- **Add the falsifier as a permanent test.** The label-shuffle control and the
  cross-split-overlap check belong in CI. They cost minutes and they are the
  only things that catch the next leak the day it is introduced.

---

## Deliverable

```
## Leakage review — <dataset> / <pipeline> @ <version>
Unit of generalization: <entity>   Time boundary: <yes/no + cutoff>
Group key: <field>   Split stored as: <artifact hash, not a seed>

### Families checked
family | checked how | result | evidence

### Falsification runs
shuffled-labels: <score vs baseline>   10%-data: <score>
group-split: <delta>   time-split: <delta>   cross-split duplicates: <n>

### Findings
<id> — family — the leaking path — which reported numbers are now void

### Structural fixes + CI controls added
### Not checked
```

## Anti-patterns

- Celebrating the jump instead of investigating it.
- Fitting the scaler, encoder, or vocabulary before the split — or once around
  a cross-validation loop instead of inside each fold.
- Storing the split seed rather than the split.
- Random splits on data with a time dimension or a repeating entity.
- Treating cross-validation as protection against leakage; it multiplies
  preprocessing leaks rather than preventing them.
- Reporting the improved number after fixing the leak, and leaving the old one
  in the README as if it had merely been superseded.
- Removing one leaking column and declaring the class closed.
- Never running the shuffled-label control, so the pipeline has never once been
  proven capable of producing a bad score.
- Reusing a public benchmark with a foundation model and reporting the result
  as a measurement rather than as an upper bound.
