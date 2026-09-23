---
name: honest-technical-oratory
description: Present a technical project out loud, under a real time limit, to an audience that may not share your vocabulary or technical background — without hyping unearned claims, without opening on caveats, and without inventing an answer live rather than saying "I don't know." Use whenever preparing or delivering a pitch, demo, talk, or hackathon presentation; whenever deciding what goes on a slide versus what stays for Q&A; or whenever a draft pitch either overclaims or buries its own value under limitations. Trigger on "pitch", "demo day", "hackathon presentation", "how should I present this", "prepare a talk", "what goes on the slides", "practice the pitch", "judges asked". Governs the live, time-boxed, spoken medium — progressive-technical-disclosure governs the written document a reader consults on demand; daubert-defensible-writing's claim discipline still applies here, just under the constraint that there is no room to attach a footnote in real time.
---

# Honest Technical Oratory

A pitch has no link to a Technical README. Whatever is said in the room is
the whole document, for as long as the room is paying attention, and it
cannot be revised after the fact. That constraint — real time, no inline
footnote, an audience that may not share your vocabulary — is what makes
this a different discipline from writing, not a shorter version of the same
one.

Composes with the library:

- **progressive-technical-disclosure** — governs the written material this
  presentation is built on and hands off to (the README, the Technical
  README); this skill governs the spoken delivery of a subset of that same
  content under a hard time limit. Don't restate that skill's ordering
  logic here — cite it for the underlying claim-ordering principle and
  apply it to what fits in the time available.
- **daubert-defensible-writing** — the claim discipline (fact / inference /
  opinion, bounded beats absolute) still governs every sentence spoken
  here. What's different is the failure mode: a written document can carry
  a footnote next to an ambitious claim; a spoken pitch cannot, so the
  claim itself has to be scoped correctly in the moment, not qualified
  after the fact.
- **non-overwhelming-ux** — a different medium (UI interaction, not spoken
  language) for the same underlying concern about cognitive load; not the
  skill to apply directly to slide/speech content, but the same instinct
  (don't make the audience hold more than they need to) transfers.

---

## The two failure directions, and why both are dishonest

**MUST NOT** hype a claim beyond what the work supports.
[YC's own demo-day guidance](https://www.ycombinator.com/blog/guide-to-demo-day-pitches/)
states this as a hard line, not a style preference: *"Exaggerations, or
worse, outright untruths, are fatal errors."* An inflated claim that a
technical judge or a follow-up question can puncture doesn't just cost that
claim — it makes every other true claim in the pitch suspect too.

**MUST NOT** open the presentation with limitations, caveats, or everything
the system doesn't do. This is the same principle
`progressive-technical-disclosure` states for a README ("narrow the claim
instead of surrounding it with disclaimers"), applied more strictly here
because the medium is stricter: a written document can put exhaustive
limitations in a linked Technical README section a reader visits when
ready; a three-minute pitch has no such room, so caveat-heavy material
belongs in Q&A or nowhere, unless it is load-bearing for a specific claim
being made in that moment — in which case it narrows that claim on the
spot, not as a preceding disclaimer.

Both directions are the same failure seen from opposite sides: substituting
a persuasion tactic (inflate, or defensively hedge) for the discipline of
stating exactly what's true, scoped to exactly what you can defend under a
hostile question.

## Structure: what earns attention, in order

Drawing on [Michael Ernst's technical-presentation
guidance](https://homes.cs.washington.edu/~mernst/advice/giving-talk.html)
and YC's pitch structure — **SHOULD** sequence a technical pitch roughly
as: the problem (stated with real weight — who has this problem and what it
costs them, not a theoretical inconvenience), why it's genuinely hard or why
it hasn't been solved this way before, the solution/demo, and a close on
a small number of memorable, concrete points. **MUST NOT** close on "future
work" as the last thing the audience hears — Ernst's point applies directly:
the last impression should be a contribution, not a list of things not yet
done.

**SHOULD** state, early and in plain language, what the project actually
does before naming the mechanism — the same problem-before-mechanism
ordering `progressive-technical-disclosure` requires of a README, compressed
into the opening lines of a talk instead of an opening section.

## Calibrating vocabulary without lying about the system

**MUST** calibrate technical depth to the audience actually in the room, not
to the most technical person imaginable in it. Ernst's framing for a mixed
technical audience: intuitions and the shape of the problem are more
valuable to most listeners than exhaustive mechanism detail — offer the
plain-language account first, and let a technical follow-up question (or an
explicit "happy to go deeper on the algorithm after") be the route to depth,
rather than delivering the depth to everyone regardless of whether they
asked.

**MUST NOT** simplify a description until it becomes false — an analogy or
plain-language account is a real, bounded model of the system, not a
description of an easier system that happens to sound similar. This is
`progressive-technical-disclosure`'s "narrow the claim" principle again,
applied to word choice: if the plain-language version can't be defended as
true under a follow-up question, it wasn't a simplification, it was a
different, easier claim standing in for the real one.

**MUST** assume that some of the audience may not share the speaker's
technical vocabulary or educational background, and design the opening
explanation accordingly — not as condescension, but as the same discipline
[plain-language guidance](https://digital.gov/guides/plain-language) applies
under the U.S. Plain Writing Act: calibrate complexity to the audience, do
not lower the substance of the content. The [Alda Method for communicating
science](https://www.aldacenter.org/about/alda-method.php) names the
specific technique: build an analogy grounded in something the audience
already has direct experience with, and read the room in real time for
whether it's landing — a technique for the live medium specifically, since a
written document can't watch its reader's face.

## Assertive, not passive, not aggressive

**SHOULD** state the work's value and its limits directly, in the
established clinical sense of assertive communication (distinct from
passive — underselling real work out of excessive hedging — and from
aggressive — dismissing a legitimate question or overselling to shut down
scrutiny). Undervaluing genuine results to seem humble is not honesty; it's
a different failure mode that produces the same outcome as
`progressive-technical-disclosure`'s caveat-first anti-pattern — an accurate
project that reads, to the room, as less than it is.

## Q&A: "I don't know" preserves credibility; improvising destroys it

**MUST** answer a question the speaker genuinely doesn't know the answer to
with an honest "I don't know" (or "I'd need to check") rather than
constructing a plausible-sounding answer live. Ernst's point stated
directly: *"Be willing to answer a question with 'no' or 'I don't know'. You
will get into more trouble if you blather on."* A wrong but confident
answer, caught later, damages every other claim made in the talk; an honest
"I don't know, let me find out" does not.

## Failure modes / anti-patterns

- **Exaggeration presented as a claim**: any statement that would not
  survive a specific, informed follow-up question — the exact failure YC
  names as fatal.
- **Caveat-first opening**: leading with limitations, non-goals, or
  disclaimers before the audience knows what was built — the oral,
  time-boxed version of `progressive-technical-disclosure`'s caveat-first
  anti-pattern, with less room to recover from it.
- **Closing on future work**: ending the talk on what isn't done yet instead
  of on the strongest true contribution made.
- **Jargon-first opening**: naming the mechanism before the plain-language
  account of what the system does and for whom.
- **A simplification that becomes a falsehood**: an analogy or
  plain-language description that can't survive a follow-up question,
  because it quietly described an easier, different system.
- **Improvised Q&A answers**: constructing a plausible response to a
  question the speaker doesn't actually know the answer to, instead of
  saying so.
- **False humility**: underselling real, demonstrated results out of
  excessive hedging — passive communication producing the same
  misrepresentation as caveat-first framing, from the opposite direction.
- **Assuming shared vocabulary**: technical terms introduced with no
  plain-language anchor, on the assumption that everyone in the room has
  the same technical or educational background as the speaker.

## Verifiable checks

- [ ] Every claim in the prepared pitch would survive a specific, informed
      follow-up question — no exaggeration that only holds up if nobody
      asks.
- [ ] The presentation opens with the problem and what it costs someone,
      not with mechanism, jargon, or limitations.
- [ ] No limitation, caveat, or non-goal is front-loaded unless it's
      load-bearing for a specific claim being made at that moment, in which
      case it narrows that claim rather than preceding it as a disclaimer.
- [ ] The close names concrete contributions, not a list of future work.
- [ ] At least one plain-language account of what the system does precedes
      any mechanism-level explanation, and that plain-language account is
      itself true, not a simpler stand-in system.
- [ ] A prepared or rehearsed Q&A includes at least one honest "I don't
      know" for a question genuinely outside what's been verified, rather
      than a filled-in plausible answer.
- [ ] The pitch states the work's real value directly — neither inflated
      past what's demonstrated, nor undersold by excessive hedging.
