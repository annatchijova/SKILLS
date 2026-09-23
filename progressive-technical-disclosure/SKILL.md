---
name: progressive-technical-disclosure
description: Order a complex technical project's presentation (a README, a hackathon submission, a project landing doc) by the reader's cognitive dependency, not by architectural importance — problem before mechanism, observable behavior before internals, evidence before technical depth. Use whenever writing or reviewing a README, a hackathon README/pitch doc, or any human-facing document that introduces a technically deep system. Trigger on "write a README", "review this README", "hackathon submission", "this reads too abstract", "where should the architecture section go", or a document that opens with implementation detail before the reader knows what problem it solves. Not a simplification skill — depth is never deleted, only routed to where the reader who wants it can find it. Governs document structure and reading order; daubert-defensible-writing governs the individual sentence's epistemic honesty within it.
---

# Progressive Technical Disclosure

This skill exists to compensate for a specific, named authorial bias:
explaining architecture, mechanism, formulas, invariants, and edge cases
*first*, because that is what feels rigorous to write, while the reader
still doesn't know what problem the project solves or why they should keep
reading. The content produced this way is often completely accurate — the
defect is ordering, not honesty, and it is a distinct defect from the ones
the rest of this library's writing skills already cover.

Composes with the library:

- **daubert-defensible-writing** — governs the sentence: fact, inference,
  and opinion never share one unlabeled sentence. This skill governs the
  document: which true, well-labeled sentence goes first, and why. A
  README can pass every daubert-defensible-writing check sentence-by-sentence
  and still fail communicatively because of *order* — that failure mode is
  this skill's territory.
- **claim-provenance-discipline** — a claim's epistemic level and scope
  bound must travel with it wherever it's placed; this skill decides
  *where* claims are placed, not how they're scoped
- **non-overwhelming-ux** — the same cognitive-load discipline that skill
  applies to interaction (chunking, one decision at a time, progressive
  disclosure of UI detail) applies to prose; cite that skill for the
  underlying rationale on scanning, chunking, and pacing instead of
  re-deriving it here
- **decision-record-discipline** — a Technical README's "design decisions
  and rejected alternatives" section *is* that skill's output, formatted
  for an external reader; don't reinvent a second decision-recording method

---

## The critical rule

> **Do not delete technical depth. Route it.**

If something is too deep for the primary document, the default move is
never to cut it — it's to place it in the document meant for depth, and
link to it precisely where a reader would want to go deeper. Depth that
disappears is a loss of rigor; depth that's placed correctly is rigor made
navigable.

## Where each claim in this skill actually comes from

Anna's explicit requirement, and the discipline this skill applies to
itself: a heuristic does not become a MUST because it sounds reasonable,
and no number below is invented (no "N bullets," no "under N words," no
claimed reader attention span) — none of that is asserted because no cited
source here actually measures it for this context.

- **Established HCI evidence**: *progressive disclosure* — Nielsen (1995,
  formalized 2006): defer secondary/advanced content to a subsidiary view,
  keep the primary view focused on what most readers need, to reduce
  cognitive load and error rate. Originally an interface-design pattern
  (a settings panel, a form); this skill applies the same mechanism to
  document architecture (primary README vs. Technical README as the
  "subsidiary screen") — that application is this skill's own
  extrapolation, not itself a Nielsen finding about documents.
- **Established documentation conventions**: the *inverted pyramid*
  (journalism convention, adopted broadly in technical-writing style
  guides): most important information first, descending. John Carroll's
  *minimalism* (task/goal-oriented technical communication, IBM Watson
  Research, 1990): lead with the reader's goal/context — the "why" — before
  procedure; strip content that doesn't serve the reader's immediate task.
- **This library's own methodological choices** (not external authority —
  Anna's design decisions for this skill specifically): the exact
  three-document architecture below, the cognitive-dependency claim-ordering
  chain, "narrow the claim instead of surrounding it with disclaimers," and
  the prohibition on feature-inventory-as-narrative. State these as house
  method, not as citing an external standard, because none exists for them.
- **No normative standard governs README structure.** Unlike WCAG for
  accessibility, there is no W3C/ISO document this skill can cite as
  binding. Everything here is evidence, convention, or house method —
  labeled as such throughout, never dressed as a requirement with borrowed
  authority.

## Document architecture

**MUST** separate three documents, each with a distinct audience:

- **`README.md`** — English, human-facing, primary. The document nearly
  everyone reads.
- **`README_ES.md`** — Spanish equivalent (a real adaptation, not a
  mechanical translation that loses the ordering discipline below).
- **Technical README** — English only, for the reader auditing or
  extending the project.

**MUST** make the three-way link immediately visible at the top of the
primary README, before any other content: `English · Español · Technical
README`. **MUST** give the Technical README link visual prominence, not
bury it in a table of contents or a footer — it is where the depth lives,
and a reader who wants to audit the project must not have to search for it.

## The reading order: claim ordering by cognitive dependency

**SHOULD** order the primary README's narrative by what a claim depends on
the reader already understanding, not by architectural importance (the
author's own default bias) and not by a fixed heading template applied
mechanically to every project:

```
problem
   ↓
mental model
   ↓
observable behavior
   ↓
differentiator
   ↓
mechanism
   ↓
evidence
   ↓
technical depth (→ Technical README)
```

Approximately, and not mechanically: Problem → What this is → Observable
behavior/demo → Why it matters → Comparison/differentiator → How it works
at a high level → Architecture → Repository tree → Evidence/results →
Try/run it → Technical deep-dive link. **MUST NOT** impose identical
headings on every project regardless of shape — the progression is the
requirement, the exact section names are not.

Three reading horizons this order is built to satisfy, progressively —
**MUST** let a reader answer each without having to read past it to the
next:

- **Seconds:** What is this? What problem does it solve? Why would I care?
- **About a minute:** What does it actually do? How does it behave? What
  differentiates it from the typical approach?
- **A few minutes:** How does it work at a high level? What did we build?
  What evidence is there that it works? How do I try it?
- **If they want more:** the Technical README.

**MUST NOT** open with an implementation-first sentence — "X is a
deterministic multi-stage architecture implementing..." — when the problem
that makes X necessary can be stated first. The problem is what earns the
reader's attention to spend on the mechanism; the mechanism cannot earn
attention for itself before the reader knows what it's for.

## Show, don't only claim

**SHOULD**, wherever the system supports it, put an observable
demonstration ahead of a list of claims about capability: if it resolves
contradictions, show a contradiction and the resolution; if it detects
something, show input → decision → evidence; if it improves a workflow,
show before → after; if a live demo exists, surface it early and
prominently. A reader who can experience the central property directly
needs less persuading than one who is told about it — and needs it
*before* being asked to understand the full architecture that produces it.

## Comparison: properties, not adjectives

**SHOULD**, where an honest and useful comparison exists, include a small
table early — `Typical approach | This project`, or the domain-appropriate
equivalent — comparing concrete, demonstrable properties and behaviors.
**MUST NOT** use unsupported marketing adjectives ("better," "advanced,"
"revolutionary") without a specific, demonstrable property standing behind
each one; if the property is demonstrable, state the property instead of
the adjective — the property is the stronger claim anyway.

## What does not open the document

**MUST NOT** front-load the primary README with the exhaustive versions of:
known limitations, non-goals, threat-model boundaries, exact reproducibility
boundaries, unsupported cases, security caveats, architectural trade-offs,
or "what this does not guarantee." Those belong primarily in the Technical
README. An accurate project preceded by several paragraphs of caveats
reads, to a first-time reader, like a system that doesn't do much — even
when every individual caveat is true and well-earned.

**This does not authorize hiding a limitation that's necessary to interpret
a claim honestly.** Never overclaim. The resolution is not to suppress the
limitation — it's to **narrow the claim instead of surrounding it with
defensive disclaimers**: say exactly what the system does, scoped
precisely enough that the statement is true without an attached paragraph
of exceptions. If a claim needs a caveat to remain honest, the caveat that's
*load-bearing for that specific claim* travels with it, narrowing it in
place — a full inventory of everything else the system doesn't do still
goes to the Technical README. This is the same discipline
`daubert-defensible-writing` states for a single sentence ("bounded beats
absolute"), applied to deciding which caveats are load-bearing enough to
stay in the primary document versus which belong in the exhaustive account.

## The repository tree: curated, not a directory dump

**MUST** annotate the repository tree with what each part is *for*, showing
conceptual architecture — not every file, cache directory, or
implementation-internal helper:

```
project/
├── core/          # deterministic decision engine
├── api/           # external interface
├── tests/         # behavioral and regression evidence
├── docs/          # technical design and decisions
└── ...
```

## Communication and cognitive load

**SHOULD** apply the same load-reduction discipline `non-overwhelming-ux`
applies to interfaces, to this document: headings that support scanning,
relatively short paragraphs, one main idea per block, diagrams used only
where they reduce explanation (not as decoration), tables for
multidimensional comparisons, code shown only when it teaches behavior,
no wall of badges, no run of a dozen-plus links before the product is
explained, no repetition of the same claim across hero/features/
architecture/conclusion, and enough whitespace/structure that the page is
navigable by eye before it's read line by line. **MUST NOT** impose an
arbitrary numeric limit (a bullet count, a word count, a section count) —
the right length is a function of the content, not a target to hit.

## Evidence discipline: capability → evidence → interpretation

**MUST** keep these three distinct for any strong claim, per
`daubert-defensible-writing`'s observation/inference/opinion layering
applied specifically to product claims:

- **Capability** — what the system does, stated precisely.
- **Evidence** — what specifically demonstrates it: the demo, the test
  suite, the benchmark, the artifact.
- **Interpretation** — what that evidence actually licenses you to
  conclude, and no more.

A benchmark states what it measured. A hash demonstrates integrity under a
stated model — not "security" as an unscoped word. A green test suite
demonstrates the properties that suite actually covers — not correctness in
general. Every strong claim in the primary README **MUST** be one of:
observable in the demo, backed by a cited test/benchmark/artifact, or
stated with exactly the scope the evidence supports — never more.

## No feature inventory as narrative

**MUST NOT** present the system as a list of features the reader has to
assemble into a system themselves:

```
Features: audit chain, MCP, REST API, spectral field, stylometry,
consolidation, crypto...
```

— true, and still the wrong shape. **MUST**, instead, first say what
system was built and why, so that when features are introduced, they
appear as the mechanisms that make the already-understood system possible,
not as an undifferentiated list the reader has to relate to each other on
their own.

## Working counter-example: where this goes wrong even with strong material

A project (`raven-memory`) opens its README with real problem framing
("Your agent has a database. It does not have a memory") — a correct
opening by this skill's own rule. The very next section is `## Architecture`,
and it goes straight to a diagram naming `KDTree`, `BFS hop`, `Ternary
scoring`, and `STDP updates` before the reader has seen a demo, a
differentiator, or a plain-language account of what the system actually
does when used. None of that technical material is wrong or unnecessary —
it belongs in the Technical README, linked from exactly the point in the
primary narrative where a reader would want to go deeper into "how." The
defect is purely where it was placed relative to problem/behavior/evidence,
and it is the case this skill exists to prevent.

## The Technical README

**MUST** contain, without softening for a general audience: architecture in
depth; exact algorithms/formulas; invariants; protocol details; threat
model; trust boundaries; security model; design decisions and rejected
alternatives (`decision-record-discipline`'s output, addressed to an
external reader); determinism/reproducibility claims with their exact
scope; benchmarks and methodology; known limitations; non-goals; failure
modes; API/protocol details where relevant; operational constraints; and
evidence/reproducibility instructions.

**MUST NOT** be made deliberately hard to read on the theory that technical
rigor requires bad prose — apply the same scanning/structure discipline
above. **MUST NOT** sacrifice precision to make it accessible to a general
audience; this is the one document in the set where the audience is assumed
to want the full, unsoftened account.

## Failure modes / anti-patterns

- **Architecture-first opening**: "X is a deterministic multi-stage
  architecture implementing..." before the reader knows what problem X
  solves.
- **Caveat-first opening**: several paragraphs of limitations, non-goals,
  and boundaries before any claim about what was actually built — technically
  honest, communicatively indistinguishable from an empty project.
- **Feature-inventory narrative**: a flat list of true capabilities with no
  stated relationship between them, leaving the reader to reconstruct the
  system themselves.
- **Adjective claims with no property behind them**: "advanced," "better,"
  "revolutionary" standing in for a demonstrable, statable property.
- **Claim repetition across sections**: the same assertion restated in the
  hero, the features list, the architecture section, and the conclusion,
  inflating length without adding information.
- **Decorative repository tree**: every `__pycache__`, build artifact, and
  internal helper listed with no annotation, burying the conceptual
  structure a reader actually needs.
- **Wall of badges / link dump before explanation**: a dozen-plus badges or
  links presented before the reader has been told what the project is.
- **Technical README that's harder to read than it needs to be**, on the
  mistaken theory that rigor and clarity trade off against each other.
- **Suppressing a load-bearing limitation** instead of narrowing the claim
  — the failure this skill's caveat-placement rule is not license for.

## Verifiable checks

- [ ] `English · Español · Technical README` (or the project's equivalent)
      is visible at the very top of the primary README, not buried.
- [ ] The primary README's opening states the problem before any
      architecture/mechanism claim.
- [ ] A reader can answer "what is this / what does it do / how is it
      different" without reading past the first few sections.
- [ ] At least one observable demonstration (input→output, before→after, a
      live demo link) appears before the deep architecture section, where
      the system supports one.
- [ ] Any comparison table states concrete properties/behaviors, not
      unsupported adjectives.
- [ ] Exhaustive limitations/non-goals/threat-model content lives in the
      Technical README; any limitation load-bearing for a specific primary-
      README claim narrows that claim in place instead of being omitted.
- [ ] The repository tree is annotated by conceptual purpose, not a full
      directory dump.
- [ ] No feature list appears before the system it belongs to has been
      explained in prose.
- [ ] Every strong claim is traceable to: an observable demo, a cited
      test/benchmark/artifact, or a statement scoped to exactly what the
      evidence supports.
- [ ] No claim is repeated near-verbatim across multiple sections purely
      for emphasis.
- [ ] The Technical README is linked prominently from the primary README,
      and specifically from the points in the narrative where a reader
      would want to go deeper — not only once at the bottom.
