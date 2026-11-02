---
name: rt-xxe
description: "Red-team assessment of XML external-entity boundaries: classic file read, blind/out-of-band and error-based XXE, parameter entities, and XXE reached through SAML, SVG, DOCX/XLSX, EPUB, SOAP and admission-webhook/CI XML. Covers parser-misconfiguration analysis, SSRF-via-XXE and billion-laughs DoS as bounded impact classes, re-expressed as owned-fixture experiments with planted files, owned OOB collectors and negative controls."
---

# XML External Entity Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's XXE craft as scoped experiments: it names the entry formats, entity techniques and parser misconfigurations to test, using planted fixture files and owned OOB collectors rather than production file reads or live internal pivots.

## Scope and prerequisites

Find every XML parse of untrusted input, including XML hidden inside other formats (SAML assertions, SVG, Office OOXML, EPUB, SOAP, RSS, `.docx`/`.xlsx`, admission-webhook payloads, CI artifacts). Use an owned instance; prove impact by reading a planted non-sensitive fixture file or hitting an owned OOB collector, never `/etc/passwd` on a real host or a real service-account token.

Declare target, parser/library and version, attempt budget, stop condition. Source-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **In-band file read** — external entity expands into the response.
- **Blind/OOB** — external DTD on an owned server triggers a parameter-entity exfil to your collector.
- **Error-based** — a crafted parameter entity leaks file content inside a parser error.
- **SSRF-via-XXE** — the entity URL points at an internal/metadata endpoint.
- **DoS** — entity expansion (billion laughs / quadratic blowup). Out of scope if the engagement excludes DoS — check the rules.

## Mechanism and observation

Trace input XML to the parser and its entity-resolution settings.

**Firstness:** Record whether a declared entity expanded (fixture content returned, owned callback hit, or error leak). **Secondness:** State the secure baseline (a hardened parser resolves no external entities) and how this deviates. **Thirdness:** Infer the defect class only after a controlled entity actually resolves.

## Abduction and refutation

**Mechanism hypothesis:** The parser resolves external/parameter entities on untrusted input, letting a declared entity read a local resource or fetch a URL.

**Competing benign explanation:** The parser has external-entity resolution disabled and the entity is inert; the "leak" is the app echoing the raw payload; the callback was an unrelated fetch; the format is parsed by a non-XML library that ignores the DTD.

## Deduction and controls

A document with only internal entities parses normally (positive control); an external-entity document must be inert if resolution is disabled. A confirmed XXE returns planted-fixture content or hits the owned collector where the internal-only control does not. Predeclare the fixture string or callback. A parser that ignores the external entity is a PASS control.

## Induction: bounded laboratory procedure

Owned instance; planted fixtures and owned collector only.

1. **Baseline.** Submit well-formed XML with an internal entity; confirm normal parsing and that the app reflects entity values.
2. **Classic read (owned).** Declare an external entity pointing at a planted non-sensitive fixture file; observe whether it expands into the response.
3. **Blind/OOB.** Host an external DTD on your owned server defining a parameter entity that exfils to your collector; submit XML referencing it; watch the collector.
4. **Error-based.** Use a parameter entity that forces the fixture content into a parser error message.
5. **Alternate entry.** Repeat through SVG upload, OOXML (`.docx`/`.xlsx` with injected XML), SAML `Content-Type`/response, SOAP — the parser, not the wrapper, is the sink.
6. **SSRF-via-XXE (owned lab).** Point the entity at an authorized internal/metadata endpoint to demonstrate the reachability class.
7. **Control.** Confirm the internal-only document is inert.

Record results including refutations. Keep finding and control status separate. If DoS is out of scope, describe billion-laughs risk from configuration rather than executing it.

## Parser and format craft

Domain knowledge to carry (leads; confirm the live library):
- Resolution defaults differ by library and version — Java (`DocumentBuilderFactory`, SAXParser, older defaults unsafe), .NET (`XmlDocument`/`XmlReader` legacy), PHP (`libxml_disable_entity_loader` history), Python (`lxml`/`xml.etree` behavior), Go. Pin the exact one.
- Parameter entities (`%`) enable blind exfil via an external DTD when general entities are filtered.
- PHP wrappers (`php://filter`) inside an entity can base64 a source file for in-band read.
- CDATA, namespace tricks and encoding (UTF-16/UTF-7) are filter-evasion families — test as filter-vs-parser differentials.
- High-value reached endpoints (bound, do not harvest): local files, internal HTTP, cloud metadata, and in Kubernetes an admission webhook parsing annotation XML → service-account token.

## Domain-specific failure modes

A reflected payload is not entity expansion. External-entity resolution disabled makes the document inert regardless of the payload's cleverness. Some stacks parse the wrapper format without a DTD-aware XML parser, so the XML sink never fires. OOB needs outbound DNS/HTTP from the parser host; a blocked egress refutes reachability, not the parser flaw.

## Evidence and deliverable

Provide the entry format, the entity construction, the planted-fixture content returned or the owned-callback record, the parser/library and version, and whether resolution was enabled. Keep real file contents out of portable output. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered formats.

## Versions and tool limitations

Pin the XML library and version — entity-resolution defaults are version-bound. Scanners may trigger DoS expansion; keep expansion bounded and respect DoS scope. No parser behavior was verified by this content; confirm the installed library first.

## Remediation and detection

Disable external-entity and DTD processing on every untrusted XML parse (library-specific hardening), prefer non-XML formats or a hardened parser, and validate wrapper formats before XML parse. Add a regression asserting an external-entity document is inert. Detect outbound requests from the parser host to file/metadata/collector-shaped URLs correlated to the request ID.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A planted fixture returns in-band or the owned collector is hit where the internal-only control is inert: CONFIRMED; FAIL (scope to what was read/reached). |
| Benign refutation | The external entity does not resolve / parser ignores the DTD: REFUTED for the tested entry; PASS for the control. |
| Insufficient evidence | Payload reflected but no expansion or callback: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-xxe/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's entry-format map, parameter-entity and error-based techniques, parser-misconfiguration knowledge and SSRF/DoS impact classes, re-expressed as owned-fixture experiments with planted files and owned collectors, replacing production file reads and live token theft with bounded reachability proof.
