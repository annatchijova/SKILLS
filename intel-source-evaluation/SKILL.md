---
name: intel-source-evaluation
description: Grade the source and the indicator before acting on either — because an indicator is not intelligence and a feed is not truth, and auto-acting on ungraded intel means blocking benign traffic, chasing decayed IOCs, and spending analyst trust on someone else's low-confidence guess. Use whenever threat intelligence arrives and something is about to act on it: "block all these IOCs", "we got a threat feed", "this indicator list from the ISAC", "is this intel reliable", "should we alert on this IOC", "the vendor says APT-X uses this", "add these to the blocklist", "how long is this IOC good for". Sibling of claim-provenance-discipline (intel is a claim that must carry its origin and confidence) and threat-attribution-restraint (the actor label attached to a feed is itself a graded claim); ranks by source reliability and indicator durability. It does not produce the intel or attribute the actor, and never auto-actions an ungraded feed as if a match were a verdict.
---

# Intel Source Evaluation

An indicator is not intelligence. A feed is not truth. "APT-X uses this IP" arriving in
a STIX bundle is a *claim*, produced by someone, with a reliability you have not yet
assessed, about an artifact whose value and shelf life you have not yet weighed. Wire
that feed straight to a blocklist and you have outsourced your firewall policy to an
anonymous analyst's low-confidence guess — and the first benign match (a CDN IP that
was a C2 three months ago, now serving half your vendors) teaches your team that the
blocklist lies.

Two independent gradings, and skipping either is how intel does damage:

- **The source** — who produced this, how reliable are they in general, and how
  credible is *this specific* report? A vendor with a strong track record can still
  ship a rushed, single-sourced advisory.
- **The indicator** — how durable and how discriminating is the artifact itself? A file
  hash costs the adversary nothing to change and matches exactly one sample; a
  behavioral TTP costs them real effort to alter and generalizes across their
  operations.

Two symmetric failure modes:

- **Block-the-feed reflex.** Auto-ingesting every IOC and blocking it, poisoning your
  own network with false positives until analysts route around the control.
- **Stale-indicator action.** Acting on a decayed artifact — a reassigned IP, a
  sinkholed domain, a hash for a sample nobody will ever send again — spending effort
  on intel whose window closed.

Composes with the library:

- **claim-provenance-discipline** — an indicator must travel with its source, confidence, and date; stripped of those it is a rumor with a firewall rule
- **threat-attribution-restraint** — the "APT-X" tag on a feed is a graded attribution claim, not a fact you inherit for free
- **daubert-defensible-writing** — "high-confidence indicator" is a claim someone will cross-examine; grade it so it survives
- **detection-engineering** — a graded, durable indicator becomes a rule with a false-positive budget, not a raw blocklist entry
- **dual-use-behavior-adjudication** — an indicator's discriminating power is a base-rate question: how many benign things also match

---

## Step 1 — Grade the source: reliability × credibility, not one number

Assess the producer and the report separately, admiralty-style, and resist collapsing
them into a single "confidence: high":

- **Producer reliability** — track record over time. Has this source's intel held up?
  Is it a primary observer or a re-packager? A well-regarded vendor, an ISAC, a
  government advisory, and a random pastebin are not interchangeable.
- **Report credibility** — for *this* item: is it corroborated, plausible, internally
  consistent, and sourced, or is it a single-sourced assertion presented with
  borrowed confidence?

A reliable source can issue a low-credibility report (early, single-sourced) and an
unreliable source can occasionally be right. Grade both axes so "trusted vendor,
therefore act" does not smuggle a weak individual claim past you.

---

## Step 2 — Grade the indicator by durability (the pyramid of pain)

Rank the artifact by how much it costs the *adversary* to change — which is inversely
how much it is worth to you:

- **Trivial to change (low value):** hashes (one bit flips them), IPs and domains
  (rotated cheaply). Useful for a short window, near-worthless as a durable control.
- **Costly to change (high value):** tools, and above all TTPs — the behaviors that
  express how the adversary operates. Expensive for them to alter, so a detection built
  on them keeps working across campaigns.

An hour spent turning a durable TTP into a behavioral detection outlasts a thousand
auto-expiring hash blocks. When a feed is all hashes and IPs, say so: it is
perishable tactical data, not strategic intelligence.

---

## Step 3 — Base-rate the indicator: how many benign things also match

An indicator's worth is not just its durability but its *discriminating power* — the
base-rate question that decides whether a match means anything:

- How many benign systems, sessions, or files also match this artifact? A "malicious"
  domain on a shared hosting provider, a JA3 hash a common library also produces, a
  user-agent string thousands of legitimate clients send — high base rate, low signal.
- An indicator that fires on benign traffic more than on the threat is not an
  indicator; it is a false-positive generator with intelligence branding. This is the
  same discipline `dual-use-behavior-adjudication` applies to behavior, applied to
  IOCs.

Where the base rate is unknown, treat the indicator as unproven and enrich before
acting — do not block first and learn the false-positive rate from the help desk.

---

## Step 4 — Decay and corroboration: an indicator has a shelf life

Two final checks before an indicator earns an action:

- **Decay / expiry.** Every atomic indicator has a window. An IP is C2 until it is
  reassigned; a domain until it is sinkholed; a hash until the sample stops circulating.
  Assign and honor an expiry; a blocklist with no expiration policy accumulates
  landmines that detonate on benign traffic months later.
- **Independent corroboration.** Five vendors repeating one original report is *one*
  source, not five. Look for genuinely independent observation before raising
  confidence, and mark daisy-chained restatements as the single source they are.

---

## Step 5 — Match the action to the grade, and ABSTAIN on ungraded intel

The action an indicator earns is a function of its two grades, not of its arrival:

- **High source + durable + discriminating + fresh** → detection or block, with a
  false-positive budget and an expiry (`detection-engineering`).
- **Weak grade / high base-rate / decayed** → enrich, watch, or drop — not block.
- **Ungraded feed** → not actionable yet. "We received the feed" is not "we can act on
  it." A documented "this feed is ungraded; not wired to blocking pending source and
  base-rate assessment" is the correct, honest posture (ABSTAIN), and it protects the
  one control every SOC actually runs on: analyst trust in its own alerts.

Every indicator that does earn an action carries its source, grade, and date with it
(`claim-provenance-discipline`), so the block is auditable and reversible when it
decays.

---

## The one-line test

If an indicator would be blocked purely because it arrived in a feed — with no grade
on the source, no weighing of how cheaply the adversary changes it, and no estimate of
how many benign things also match — you are not acting on intelligence, you are
laundering an anonymous guess into a firewall rule that your analysts will learn to
distrust.
