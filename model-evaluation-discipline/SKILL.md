---
name: model-evaluation-discipline
description: Build a model evaluation that can actually fail — a mandatory baseline, a metric that matches the decision the output feeds, an interval instead of a point estimate, a test set treated as a consumable, subgroup breakdowns that expose what the aggregate hides, and negative controls that prove the pipeline is capable of producing a bad score. Use whenever a model is evaluated, compared, promoted, or reported, and whenever a number is used to justify shipping. Trigger on "accuracy", "F1", "AUC", "our model gets X%", "it beats the baseline", "which model should we ship", "the metric improved", "evaluate this model", "benchmark", "is this good", "calibration", "the offline numbers looked fine", "SOTA", or a model comparison with one number per model. Sibling of falsifiable-testing, which governs tests that can fail; this one governs metrics that can fail. It does not tune models and does not chase leaderboard positions.
---

# Model Evaluation Discipline

An evaluation that cannot produce a bad number measures nothing. This is
`falsifiable-testing`'s thesis moved into a domain where it is violated by
default, because the standard evaluation is a single aggregate number, computed
against no baseline, on a set that has been looked at two hundred times, with no
interval and no breakdown.

The number that comes out of that is not a measurement. It is a summary of
choices that were made while looking at it.

Three questions, in this order, before any evaluation number is quoted:

> **Compared to what?** (the baseline)
> **How much of this is noise?** (the interval)
> **Who does it fail for?** (the breakdown)

Composes with the library:

- **falsifiable-testing** — oracle strength, negative controls, seeing red first
- **data-leakage-hunting** — a leak corrupts every number here; the baselines in
  Part 1 are often what makes it visible
- **training-run-provenance** — the seed spread that turns a point estimate into
  an interval
- **llm-out-of-the-loop** — if the score feeds a deterministic decision rule,
  calibration is a correctness property, not a nicety
- **honest-degradation** — a model that abstains is often better than one that
  guesses confidently
- **daubert-defensible-writing** — how the number is worded when it travels

---

## Part 1 — The baseline is not optional

A metric without a baseline carries no information. Compute at least these, and
report them beside the model, always:

- **Majority class / constant prediction.** 94% accuracy at 94% prevalence is
  zero information, and it is the most common way a useless model ships.
- **Random**, respecting the class distribution.
- **The existing system** — the heuristic, the rule, the human, the regex, the
  thing you are proposing to replace. This is the only baseline the business
  actually cares about.
- **The trivial model** — logistic regression on three features, or "predict
  the previous value" for anything with a time dimension. If it matches the
  large model, ship it and keep the week you were about to spend.

The baselines have a second job: they are leak detectors. A trivial baseline
that scores far too well means the task is being solved by something other
than the signal you think you found (`data-leakage-hunting`).

## Part 2 — The metric has to match the decision

Pick the metric from what happens to the output, not from convention:

- **Imbalanced classes** → accuracy is meaningless; use precision/recall,
  PR-AUC, or the cost-weighted metric.
- **Asymmetric error costs** → decide the operating point by what each error
  actually costs, not at the default threshold. A false negative in fraud and a
  false positive in fraud are not comparable quantities, and no single number
  makes them so.
- **A ranking is consumed** → ranking metrics at the depth people actually
  look at, not over the full list.
- **The score becomes a probability or crosses a threshold** → **calibration is
  a correctness property.** A model can rank perfectly and be badly calibrated;
  when a downstream rule compares its score to a fixed number, miscalibration is
  a silent decision bug, not a modeling nicety. Report a calibration curve
  whenever a threshold exists.
- **Abstention is possible** → measure coverage and the accuracy on what it did
  answer. A model that declines the hard 5% is often the right product
  (`honest-degradation`).

And evaluate **the decision, not the model**. If the model's output enters a
pipeline with a threshold, a business rule, and a fallback, then the number that
matters is the outcome of that whole path — not the model's isolated AUC.

## Part 3 — A point estimate is not a result

Two models differing by 0.3% when the seed-to-seed spread is ±1.5% are the same
model, and every hour spent choosing between them is wasted.

- Report an **interval**: across seeds (`training-run-provenance`), across
  bootstrap resamples of the test set, or both. They measure different things —
  training variance and evaluation-set variance — and both matter.
- **The comparison needs the spread of the thing being compared to.** "A beats
  B" requires B's variance, not just B's number.
- On a small test set, the confidence interval is often wider than every
  difference in your comparison table. Compute it before building the table.

## Part 4 — The test set is a consumable

Every look spends it. This is the slowest form of leakage and the hardest to
notice, because no single peek feels like cheating.

- **Iterate on validation.** The test set is opened when a decision is final.
- **Count the evaluations** and report the count. "Evaluated on the test set
  three times" is a meaningful disclosure; a hundred is a different claim.
- **When it is spent, get a fresh one** — a later time slice, a new collection,
  a held-back shard opened once. For anything that ships, a **temporally fresh**
  set is the only honest final number, because it is the only one that also
  tests for drift.
- Anything chosen by looking at the test set — a threshold, an early-stopping
  point, a feature set, an architecture — is fitted to it. Fit those on
  validation.

## Part 5 — Aggregates hide exactly what you need to know

The mean is the number least likely to describe anyone's experience.

- **Break down by subgroup and slice**: by class, by segment, by input length,
  by source, by device, by language, by time period, by difficulty. **Report the
  worst slice**, not only the average. A model at 95% overall and 61% for one
  population is a 61% model for that population.
- **Break down by time.** A metric that decays across the evaluation window is
  drift already visible in your offline data.
- **Read fifty errors by hand.** It is the highest-value hour in applied ML and
  the one most consistently skipped. Aggregate metrics tell you how much is
  wrong; only the examples tell you *what kind* of wrong, and the kind is what
  determines the fix.

## Part 6 — Negative controls: prove the evaluation can fail

Straight from `falsifiable-testing`, and rarely run:

| Control | Expected | If it fails |
|---|---|---|
| **Shuffle the labels**, retrain | performance falls to baseline | leakage or a pipeline bug — stop everything |
| **Train on 10% of the data** | clearly worse | the task is not being solved by learning |
| **Ablate each feature group** | proportionate degradation | a single feature carrying the label |
| **Corrupt the input at inference** | performance falls | the model is ignoring the input path you think it uses |
| **Evaluate an untrained model** | baseline performance | the evaluation harness is scoring something else |

That last one catches an entire genre of harness bug: labels misaligned with
predictions, the wrong split loaded, a metric computed over the wrong axis. Run
it once per harness, not once per model.

## Part 7 — What the offline number cannot see

State the gap explicitly rather than letting the reader assume there is none:

- **Feedback loops** — the model changes the data it is later evaluated on.
- **Selection bias in logged data** — you only observe outcomes for the actions
  the previous system took.
- **Distribution shift** between the evaluation window and deployment.
- **The action is not the prediction** — outcomes depend on what someone does
  with the output, which the offline set never recorded.

None of these are solved here. They are named here so the offline number is
quoted as what it is.

---

## Deliverable

```
## Evaluation — <model> <version>
Task | decision the output feeds | metric and why that metric
Test set: <version, hash>  |  evaluations spent: <n>  |  freshness: <window>

| system | metric [interval] | worst slice | calibration |
| majority-class baseline | | | |
| existing system | | | |
| trivial model | | | |
| this model | | | |

Seed spread: <±>   Bootstrap CI: <±>   Δ vs baseline: <inside/outside noise>
Negative controls: shuffled-labels <x> | 10%-data <x> | untrained <x>
Breakdown: <worst subgroup and its number>
Error analysis: <n examples read by hand, the failure kinds found>
Offline blind spots: <feedback loops, selection bias, shift>
```

## Anti-patterns

- Reporting a metric with no baseline.
- Accuracy on imbalanced data.
- One number per model in a comparison table, with no interval anywhere.
- Declaring a winner on a difference smaller than the noise.
- Tuning thresholds, early stopping, or feature selection on the test set.
- Comparing against a number from someone else's paper, on their split, on
  their data version.
- Reporting the mean and never looking at the worst slice.
- Never reading actual errors.
- Treating a well-ranked but uncalibrated score as safe to threshold.
- Evaluating the model in isolation when a whole pipeline makes the decision.
- Never running a negative control, so the harness has never been shown capable
  of producing a bad number.
