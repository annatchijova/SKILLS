---
name: rt-deserialization
description: "Red-team assessment of insecure-deserialization boundaries across Java (ObjectInputStream, XMLDecoder, Jackson/JNDI), PHP (serialize, phar), .NET (BinaryFormatter, Json.NET TypeNameHandling, ViewState), Python (pickle, unsafe YAML), Node (node-serialize) and Ruby (Marshal). Covers format recognition signatures and gadget-chain reasoning, re-expressed as owned-fixture experiments using detection-only gadgets (URLDNS/owned-callback) and negative controls instead of RCE payloads."
---

# Insecure Deserialization Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's deserialization craft as scoped experiments: it names the formats, sinks and gadget families, and proves reachability with detection-only gadgets (a DNS lookup to an owned collector) rather than shipping RCE gadget chains against a target.

## Scope and prerequisites

Find every sink that deserializes untrusted bytes: cookies, POST bodies, hidden fields, caches (Redis/Memcached), queues (Celery/RabbitMQ), session stores, ViewState, JMX/RMI. Use an owned instance with the same library versions; confirm reachability with a safe gadget that only makes an owned DNS/HTTP callback (e.g. URLDNS-style), never an RCE chain.

Declare target, language/library and exact versions (gadget availability is version- and classpath-bound), attempt budget, stop condition. Source-only authorization yields a hypothesis marked NOT TESTED. RCE via gadget chain is an impact class to demonstrate on an owned lab, bounded, not run live.

## Attack surface and recognition signatures

Recognize the format first (leads):
- Java `ObjectInputStream`: hex `ac ed 00 05`, Base64 `rO0AB`. XMLDecoder: `<java>`/`<object class=`.
- PHP serialize: `O:<len>:"Class":` / `a:<count>:{`, often Base64 in cookies. phar: polyglot disguised as an image.
- .NET BinaryFormatter: Base64 `AAEAAAD/////`; Json.NET: `"$type":`; ViewState blobs.
- Python pickle: opcodes `\x80\x04\x95` (v4+) / `(dp0`; found in Redis, Celery, ML pipelines.
- Ruby Marshal: `\x04\x08`. Jackson polymorphic: `["class.name", {`.

## Mechanism and observation

Trace untrusted bytes to the deserializer and its type controls (filters, allowlists, `enableDefaultTyping`).

**Firstness:** Record whether a detection gadget triggered (owned DNS/HTTP callback) and the deserializer's errors. **Secondness:** State the secure baseline (type-restricted or signed/opaque data only) and the deviation. **Thirdness:** Infer the defect class only after a controlled gadget resolves.

## Abduction and refutation

**Mechanism hypothesis:** The sink reconstructs attacker-chosen types from untrusted bytes with no type restriction, so a gadget present on the classpath executes during deserialization.

**Competing benign explanation:** The blob is HMAC-signed and tampering is rejected before deserialization; an `ObjectInputFilter`/allowlist blocks the type; the required gadget is not on the classpath; the data is opaque/encrypted; the value is parsed by a safe format, not deserialized.

## Deduction and controls

A valid signed/typed object deserializes (positive control); an attacker-typed object must be rejected if controls hold. A confirmed finding fires the owned callback via a detection gadget where the control object does not. Predeclare the callback. A signature check or type filter rejecting the object is a PASS control.

## Induction: bounded laboratory procedure

Owned instance, version-matched; detection-only gadgets.

1. **Baseline.** Capture a legitimate serialized object; confirm the sink deserializes it and note any signature/MAC.
2. **Signature check.** Flip a byte; if it is rejected intact, a MAC likely gates the sink — record as a control.
3. **Detection gadget (owned).** Submit a gadget that only performs a DNS/HTTP lookup to your collector (Java URLDNS, equivalent benign chains elsewhere). A callback proves the bytes were deserialized into attacker-chosen behavior — without RCE.
4. **Classpath/type mapping.** From source or errors, enumerate available gadget libraries (Commons-Collections, Spring, Hibernate, BeanUtils; phpggc chains; ysoserial.net families) — knowledge, not execution.
5. **Impact bound (owned lab).** If demonstrating RCE reachability is in scope, do it once on the owned lab with a benign marker, then stop.
6. **Control.** Confirm the signed/typed control path rejects the attacker object.

Record results including refutations. Keep finding and control status separate.

## Gadget-family craft (leads; impact classes to bound)

- **Java** — ysoserial families (CommonsCollections 1-7 by JDK/version, Spring, Hibernate, BeanUtils), JRMPClient/JNDI redirect, Jackson polymorphic + JNDI, XMLDecoder. Use URLDNS for safe confirmation first.
- **PHP** — phpggc (Laravel, Symfony, Monolog, Guzzle, WordPress), phar:// triggering via file-ops functions.
- **.NET** — ysoserial.net (TypeConfuseDelegate, WindowsIdentity, TextFormattingRunProperties, PSObject), ViewState when machine key is disclosed, Json.NET `TypeNameHandling`.
- **Python** — pickle `__reduce__`, unsafe `yaml.load`.
- **Node** — `node-serialize` IIFE, `funcster`. **Ruby** — Marshal gadget chains.

## Domain-specific failure modes

A signed blob makes the sink unexploitable without the key — report that as a control, not a bypass. Gadget availability is classpath- and version-specific; absence of a chain is not absence of the flaw (and vice versa). A callback proves deserialization reachability; RCE still depends on an available gadget. Modern filters (`ObjectInputFilter`, `TypeNameHandling=None`) change the verdict — verify them.

## Evidence and deliverable

Provide the sink, the format signature, the detection-gadget callback record, the library/versions and classpath evidence, and any signature/type control. Keep host output out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered sinks.

## Versions and tool limitations

Pin library and runtime versions and the classpath — gadget chains are version-bound. ysoserial/phpggc/ysoserial.net default to RCE payloads; use detection-only gadgets for confirmation and bound any RCE demo to an owned lab. No chain was verified by this content; confirm versions first.

## Remediation and detection

Do not deserialize untrusted data; prefer data-only formats (JSON without polymorphic typing); if unavoidable, HMAC-sign blobs, apply strict type allowlists (`ObjectInputFilter`, `TypeNameHandling=None`), and isolate the process. Add a regression asserting the detection gadget is rejected. Detect unexpected class loads and outbound callbacks during deserialization correlated to the request ID.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A detection gadget fires the owned callback where the control object is rejected: CONFIRMED for deserialization reachability; FAIL (RCE only if an available gadget is shown). |
| Benign refutation | A signature check or type filter rejects the attacker object: REFUTED for the tested sink; PASS for the control. |
| Insufficient evidence | Format recognized but no callback and no type-control visibility: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-deserialization/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's format-recognition signatures and cross-language gadget-family knowledge, re-expressed as owned-fixture experiments using detection-only gadgets and signature/type controls, replacing RCE gadget chains with bounded reachability proof.
