---
name: parser-differential-hunting
description: Hunt the bugs that live where two components read the same bytes and disagree about what they mean — the validator parses one way, the executor another, and the attacker writes input that is two things at once. Use whenever a value crosses a component, language, or process boundary and is re-interpreted — proxy in front of an app server, gateway before a backend, WAF before a handler, client validation before server storage, signature verified before content is re-parsed, or one format embedded in another. Trigger on "request smuggling", "path traversal", "canonicalization", "normalization", "Unicode/homoglyph/punycode/IDN", "duplicate keys", "content-type sniffing", "URL parsing", "the proxy and the backend disagree", "it validated but stored something else", "double decode", "polyglot", "type confusion", or two parsers of the same format appearing in one system. Expands invariant-hunting's semantic-boundary family into a full method; hands verdicts to discriminating-proof.
---

# Parser Differential Hunting

Every checkpoint in a system parses the input in order to decide about it, and
then hands the *original bytes* onward to something that parses them again.
The check is only as good as the assumption that both parses agree. They
frequently do not, and the gap is not a bug in either parser — each is locally
reasonable. The bug is in the composition, which means neither team owns it and
neither test suite covers it.

The question this skill asks, at every boundary:

> **Two components read these same bytes. Under what input do they disagree —
> and is the disagreement between the component that *decides* and the
> component that *acts*?**

Only that second half makes a differential a vulnerability. `A` and `B`
disagreeing is a curiosity; `A` authorizing on its reading while `B` executes
on a different one is an authorization bypass with no missing check anywhere.

Composes with the library:

- **invariant-hunting** — this skill is the deep method for its family #4
  (semantic boundary failure); the invariant here is
  `meaning_at_checkpoint == meaning_at_sink`
- **oracle-driven-fuzzing** — two parsers *are* the differential oracle; this
  skill says which pairs to point it at
- **validate-at-the-boundary** — the fix side: parse once, forward the parsed
  form, never the bytes
- **discriminating-proof** — earns the verdict on a candidate disagreement
- **reverse-engineering** — when one of the two parsers is closed

Authorization: hunt systems you own or are authorized to test. The comparison
work — running two parsers over the same corpus offline — is safe anywhere; the
end-to-end confirmation is a live test and needs scope.

---

## Part 1 — Find the parser pairs

Draw the byte's journey and mark every place it is *interpreted*. A pair exists
wherever the same bytes are interpreted twice by different code. High-density
habitats, in rough order of yield:

| Pair | The bytes | Classic disagreement |
|---|---|---|
| Proxy / origin server | HTTP framing | `Content-Length` vs `Transfer-Encoding`, duplicate headers, obsolete line folding |
| WAF or validator / handler | body, query string | one decodes `%2e%2e`, the other does not |
| Router / filesystem | path | `..`, `.`, `//`, trailing dot, `\` on Windows, symlink resolution |
| Auth check / storage layer | identifier | case-insensitive lookup vs case-sensitive write; trailing whitespace |
| JSON parser A / JSON parser B | document | duplicate keys (first vs last wins), big integers, `NaN`, comments |
| Signature verifier / consumer | signed blob | signature over the canonical form, consumption of the raw form |
| Serializer / deserializer | object graph | round-trip is not identity (`oracle-driven-fuzzing` rung 3) |
| Allowlist matcher / HTTP client | URL | userinfo `@`, fragment, port, IPv6 brackets, DNS rebinding — the matcher's host is not the client's host |
| Template / renderer | markup | one escapes, the other re-parses the escaped form |
| Archive lister / extractor | entry names | absolute paths, `..`, symlinks — name shown is not name written |
| Client validation / server | form data | never a security boundary; verify the server repeats it |

Two parsers written in different languages, by different vendors, at different
times, for the same format are the ideal candidate. So is any format embedded
in another (JSON in a header, a URL in a query parameter, base64 wrapping
anything) — every layer of encoding is another chance to disagree.

## Part 2 — The disagreement families

Name the family before testing; each has a known generator.

1. **Ambiguity in the format.** The spec permits two readings, or is silent.
   Duplicate fields, conflicting length indicators, optional whitespace.
2. **Different strictness.** One parser rejects, the other repairs. The
   permissive one usually sits behind the strict one — which means the strict
   one is the checkpoint and never sees what the permissive one will make of
   the input.
3. **Different canonicalization order.** Decode-then-normalize versus
   normalize-then-decode. Any pipeline that does both in a different order is a
   candidate by construction.
4. **Different alphabet.** Unicode normalization, case folding (the Kelvin sign
   folds to `k`), overlong UTF-8, homoglyphs, zero-width and bidirectional
   characters, punycode. Case-insensitive comparison or NFKC normalization
   applied at only one end is the recurring bug.
5. **Different truncation point.** Null bytes, newlines, length limits: one
   component sees `evil.example\0.trusted.example` as one string, the other
   stops at the null. A database column that silently truncates at 255 is the
   same bug in slow motion.
6. **Different type coercion.** `"1"` versus `1`, `"false"` truthiness, arrays
   where scalars were expected, `null` versus absent. Two languages' coercion
   rules are never the same.
7. **Sniffing over declaration.** One component believes the declared
   `Content-Type`, the other sniffs the content. Polyglot files exist because
   of this.

## Part 3 — The method

The comparison is cheap and offline; run it before any live testing.

1. **Extract both parsers into one harness.** Import the library the proxy uses
   and the one the app uses; or shell out to both. The harness takes bytes and
   returns each parser's *decision-relevant projection* — the host it resolved,
   the path it produced, the map it built, the length it framed.
2. **Compare the projection, not the whole output.** Two JSON parsers differ in
   a dozen irrelevant ways. Compare only what the checkpoint decides on.
3. **Seed with the format's known-hard corners** (Part 2's families), then let
   `oracle-driven-fuzzing` run the search with `A(x) != B(x)` as the oracle.
   This is among the strongest oracles in the library: it needs no ground truth
   and no notion of "correct".
4. **Triage each disagreement by position.** For every differing input, ask
   which parser is the *decider* and which is the *actor*. A disagreement in
   which the actor is the stricter of the two is inert. Only
   `decider says safe → actor does something else` is a finding.
5. **Confirm end to end.** A harness-level disagreement is a *plausible
   hypothesis*: the real pipeline may normalize between the two, or reject
   earlier. Send the input through the real path and observe the actor's
   behavior (`discriminating-proof` — binary oracle, plus a negative control
   that is byte-identical except for the ambiguity).

## Part 4 — The fix is architectural, and this is the blue payoff

Point fixes ("also reject `%2e%2e`") lose, because the next encoding is always
one layer deeper. Rank the remediations you propose:

1. **Parse once, forward the parsed form.** The checkpoint emits a structured,
   unambiguous representation and the actor consumes *that*, never the original
   bytes. This deletes the class rather than one instance.
2. **One parser, shared.** Both components call the same library at the same
   version. Cheap when both sides are yours.
3. **Reject ambiguity instead of resolving it.** Duplicate header, two length
   indicators, non-NFC input, a path containing `..` before resolution → 400.
   A format's ambiguous corner is almost never legitimate traffic; refusing it
   costs little and removes the disagreement's fuel.
4. **Canonicalize in exactly one place, then compare canonical to canonical** —
   and pin the order: decode to a fixpoint, then normalize, then validate, then
   use the validated value and nothing else.
5. **Only then**, filters and signatures over the raw bytes.

Also hand the pair to `detection-engineering`: "requests where the front-end
and back-end interpretations differ" is a high-signal, low-volume detection,
and one of the few that is nearly free of false positives.

---

## Anti-patterns

- Comparing full parser outputs, drowning the real disagreement in noise.
- Reporting a harness-level disagreement as a vulnerability without tracing it
  to a decider/actor split in the live pipeline.
- Assuming the strict parser protects the permissive one — it is usually in
  front of it, deciding about bytes it will never execute.
- Fixing one encoding and declaring the class closed.
- Trusting client-side validation as one half of the pair. It is not a
  checkpoint; it is a hint.
- Normalizing after the authorization check instead of before it.
- Treating "both are spec-compliant" as a reason not to file it. The
  composition is the bug; compliance of the parts is why it survived.
