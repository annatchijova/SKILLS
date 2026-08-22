# SKILLS — Engineering Discipline Skill Set

A collection of 46 skills for Claude Code that encode disciplined software engineering, forensic reasoning, and security-first construction. Each skill activates automatically when the conversation matches its trigger conditions, injecting methodology without requiring the user to ask for it.

These skills form a coherent system built on Charles Sanders Peirce's triadic semiotics and the abductive inference loop (abduction → deduction → induction). They cover the full engineering lifecycle: investigation, construction, patching, testing, auditing, and hardening.

---

## Skills

| # | Skill | Category | Activates when |
|---:|---|---|---|
| 1 | `abductive-engineering` | Core reasoning | Debugging, root-cause analysis, incident response, or architectural decisions under uncertainty. |
| 2 | `red-team-auditing` | Core reasoning | Security audits, adversarial review, threat modeling, or invariant analysis. |
| 3 | `secure-by-construction` | Core reasoning | Writing, extending, refactoring, or reviewing code with security boundaries. |
| 4 | `software-archaeology` | Core reasoning | Modifying legacy, inherited, or unfamiliar code without breaking behavior. |
| 5 | `diagnosing-bugs` | Core reasoning | Investigating hard bugs and performance regressions through controlled probes and regression tests. |
| 6 | `codebase-health-assessment` | Core reasoning | Classifying dead, fossil, live, and out-of-scope modules before changing a codebase. |
| 7 | `reverse-engineering` | Core reasoning | Reconstructing undocumented systems, binaries, protocols, file formats, or opaque APIs without readable source. |
| 8 | `daubert-defensible-writing` | Core reasoning | Writing findings and reports that separate evidence, inference, uncertainty, and opinion. |
| 9 | `deterministic-core` | Determinism & integrity | Producing bit-for-bit reproducible and tamper-evident decisions with canonical serialization and SHA-256 sealing. |
| 10 | `llm-out-of-the-loop` | Determinism & integrity | Keeping consequential decisions outside the LLM path and sealing results before optional narration. |
| 11 | `tamper-evident-audit-chain` | Determinism & integrity | Building or verifying append-only logs that detect alteration, insertion, reordering, or deletion. |
| 12 | `atomic-state-mutation` | Determinism & integrity | Making multi-write persistent operations all-or-nothing and isolated from concurrent callers. |
| 13 | `versioned-schema-evolution` | Determinism & integrity | Evolving serialized artifacts with explicit schema versions without breaking existing data. |
| 14 | `surgical-patcher` | Patching & editing | Applying anchored, verified, reversible changes instead of rewriting entire source files. |
| 15 | `audit-before-patch` | Patching & editing | Validating an audit finding against the current file before changing any code. |
| 16 | `validate-at-the-boundary` | Input & data | Validating untrusted input at the system boundary with clear errors. |
| 17 | `honest-degradation` | Input & data | Handling degraded, legacy, reconstructed, or unverifiable input without returning plausible-looking wrong results. |
| 18 | `sql-aggregation-not-materialization` | Input & data | Pushing counts, sums, and grouping into the database instead of loading rows into memory. |
| 19 | `git-discipline` | Process | Keeping AI-assisted coding sessions recoverable, reviewable, and free from unsafe history rewriting. |
| 20 | `claim-provenance-discipline` | Evidence governance | Preserving each claim's origin, epistemic level, scope bound, and falsifier across summaries and handoffs. |
| 21 | `attack-surface-triage` | Adversarial validation | Enumerating an authorized target's surface into a reproducible, falsifiable candidate queue — before any payload. |
| 22 | `purple-team-exercise` | Adversarial validation | Turning each technique into a detection hypothesis, detonating it minimally and marked, and measuring what the blue side saw. |
| 23 | `detection-engineering` | Adversarial validation | Turning a detection requirement into a tested, budgeted, versioned rule — with a benign twin that must not fire. |
| 24 | `agent-trust-boundaries` | Agent architecture | Keeping retrieved content as data, tool authority in deterministic policy, and the untrusted/private/egress trifecta broken. |
| 25 | `falsifiable-testing` | Verification | Writing tests that can actually fail — red first, negative controls, oracle strength, and flakes treated as findings. |
| 26 | `incident-timeline-reconstruction` | Evidence governance | Ordering events across clock domains, separating recorded from actual time, and labeling every gap by kind. |
| 27 | `irreversible-action-gate` | Process | Classifying actions by reversibility and blast radius, then gating them with preview, count assertion, and a written undo plan. |
| 28 | `dependency-provenance` | Supply chain | Knowing what is actually shipped, establishing package identity before trust, and treating advisories as candidates until reachability is shown. |
| 29 | `secret-lifecycle-discipline` | Credentials | Treating credentials as a lifecycle — redaction at the boundary, rotation rehearsed before it is needed, rotate-first on exposure. |
| 30 | `decision-record-discipline` | Process | Capturing forces, rejected alternatives, load-bearing assumptions, and revisit triggers while the context still exists. |
| 31 | `concurrency-reasoning` | Core reasoning | Reasoning about shared mutable state, invariants, and happens-before ordering instead of adding a lock and hoping. |
| 32 | `forensic-logging-design` | Evidence governance | Deciding what to record today so tomorrow's reconstruction is possible — decisions, correlation, and legible silence. |
| 33 | `invariant-hunting` | Core reasoning | Hunting violations of a declared or implied security invariant across a transition — a property established at T0 that a later state change must preserve. |
| 34 | `beyond-the-sink` | Core reasoning | An investigation stalls — looking past the sink-grep keyword list, the exhausted question family, or a single implementation when the obvious layer is dry. |
| 35 | `discriminating-proof` | Verification | Turning a plausible hypothesis into an earned verdict with the cheapest experiment that can kill it — binary oracle, canary value, negative control. |
| 36 | `forensic-persistence` | Core reasoning | A hunt, audit, or debug session returns zero findings, hypotheses keep getting refuted, or a target looks too hardened to continue. |
| 37 | `oracle-driven-fuzzing` | Verification | Bugs must be found by generated input — property-based, structure-aware, differential and metamorphic oracles, corpus discipline, shrinking, and crash triage. |
| 38 | `parser-differential-hunting` | Adversarial validation | Two components read the same bytes and disagree — the checkpoint decides on one meaning while the sink acts on another. |
| 39 | `authorization-surface-mapping` | Adversarial validation | Building the actor × resource × action matrix and testing the cells nobody wrote a test for — because a missing check looks like nothing. |
| 40 | `assume-breach-modeling` | Adversarial validation | A position is already held — mapping what that identity reaches, and finding the choke point whose removal cuts the most paths. |
| 41 | `resource-exhaustion-review` | Input & data | A small input buys a large amount of work or memory — asymmetry ratios, unbounded allocation, super-linear algorithms, missing backpressure. |
| 42 | `remediation-driven-reporting` | Adversarial validation | Writing the report so the class gets fixed, not the instance — surviving triage, severity scored to demonstrated impact, and verifying the patch against the class. |
| 43 | `finding-custody` | Evidence governance | A confirmed finding after it is reported — instance vs class vs method, the patch-diffing window, custody of the PoC, and a disclosure decision with a revisit trigger. |
| 44 | `data-leakage-hunting` | Machine learning | The one bug class whose symptom is a better score — evaluation data reaching the model through preprocessing, time, groups, duplicates, or a spent test set. |
| 45 | `training-run-provenance` | Machine learning | Determinism where it is achievable — the artifact, not the process: a sealed manifest, named nondeterminism, and a reproducibility claim at the rung the evidence supports. |
| 46 | `model-evaluation-discipline` | Machine learning | An evaluation that can actually fail — mandatory baseline, interval instead of point estimate, worst slice instead of mean, and negative controls. |

### Adversarial validation loop

`attack-surface-triage` opens the loop and `red-team-auditing` is the
confirmation step; the hunting skills feed candidates in, and the impact and
containment skills carry a confirmed finding back out to the blue side:

```
                 attack-surface-triage → ranked candidates
                              │
   ┌──────────────────────────┼──────────────────────────┐
   │  where candidates come from (the hunt)              │
   │  invariant-hunting · parser-differential-hunting    │
   │  authorization-surface-mapping · beyond-the-sink    │
   │  oracle-driven-fuzzing · resource-exhaustion-review │
   └──────────────────────────┼──────────────────────────┘
                              ▼
      discriminating-proof → red-team-auditing → confirmed / refuted
                              │                        │
                              │            forensic-persistence (refuted → next axis)
                              ▼
      assume-breach-modeling → impact, choke points, containment
                              ▼
      purple-team-exercise → detection gaps
                              ▼
      detection-engineering → proven rule → (retest closes the loop)

   when the target is someone else's:
      remediation-driven-reporting → the class gets fixed, not the instance
      finding-custody → what you did NOT say, and what reopens the decision
```

Everything on the offensive side of this library exists to produce a defensive
artifact: a bound, a bulkhead, a generated negative test, or a rule that has
fired for the right reason.

### The machine-learning seam

ML breaks three assumptions the rest of the library rests on: the test is a
metric rather than a pass/fail, the data is the real program, and the
highest-severity bug class *raises* the score. Skills 44–46 restore them, and
they meet `deterministic-core` at a specific boundary:

```
training run        →   frozen artifact   →   inference   →   decision
nondeterministic        hashed, immutable     deterministic     exact
training-run-           the seam              same artifact     deterministic-core
provenance                                    + input           applies unmodified
       ↑                                            ↑
data-leakage-hunting                    model-evaluation-discipline
(is the number real?)                   (is the number a measurement?)
```

Determinism does not stop being reachable in ML — it stops being reachable
*upstream of the artifact*. Everything downstream is held to the same standard
as any other consequential output path here.

---

## Repository Structure

Each skill lives in its own directory and is a single self-contained file:

```
<skill-name>/
  SKILL.md      # YAML frontmatter (name + description) followed by the full methodology
```

The `description` field is the trigger surface — it must name the situations,
phrasings, and artifacts that should activate the skill, and it must stay under
1024 characters. The body is loaded only once the skill triggers.

No skill currently ships `scripts/` or `references/` subdirectories; add them
alongside `SKILL.md` if a future skill needs executable helpers or long reference
material that does not belong in the always-loaded body.

---

## Design Principles

- **No LLM in the decision path.** Consequential outputs are sealed deterministically before any model is called.
- **Abduction before deduction.** Every diagnosis generates a falsifiable hypothesis, derives a testable prediction, and confirms or refutes it against the real system.
- **Eco's razor.** Before acting on any hypothesis, attempt to refute it. A refuted hypothesis is a result, not a failure.
- **Honest degradation over false confidence.** Three states, not two: PASS / WARN / FAIL. ABSTAIN is a valid verdict.
- **Surgical patching over rewriting.** Regenerating a file from memory is the largest source of silent regressions.
- **Never trust a green you have not seen red.** A test — or a detection rule — that has never failed for the right reason measures nothing.
- **Authority comes from the channel, not the content.** Retrieved documents, tool output, and other agents' summaries are data; none of them can grant themselves permission.
- **Proportional gates before irreversible actions.** Preview the exact targets, assert the expected count before seeing it, and write the undo plan before acting — not after.
- **Red exists to produce blue.** A confirmed finding is not the deliverable; the bound, the bulkhead, the generated negative test, and the detection requirement are.
- **You cannot grep for an absence.** Missing checks, unenumerated cells, and unstated limits are invisible in a diff — they are found by enumerating what the system claims to enforce and testing the gaps.
- **A finding is not finished when it is patched.** The instance dies with the fix; the class does not. Reporting, custody, and the decision not to publish all have their own discipline.
- **A result that looks too good is a bug report.** In every other domain a defect makes something fail; leakage makes everything look better, so the alarm has to be inverted.

---

## Related

- [vigia-intent-analysis](https://github.com/annatchijova/vigia-intent-analysis) — VIGÍA forensic intent analysis engine (SANS FIND EVIL Hackathon 2026). These skills encode its engineering invariants.

---


                    ┌─────────────────────────┐
                    │     INQUIRY / REASONING │
                    │                         │
                    │ abductive-engineering   │
                    │ diagnosing-bugs         │
                    │ software-archaeology    │
                    │ reverse-engineering     │
                    │ invariant-hunting       │
                    │ concurrency-reasoning   │
                    │ beyond-the-sink         │
                    │ forensic-persistence    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   ADVERSARIAL VALIDATION│
                    │                         │
                    │ attack-surface-triage   │
                    │ red-team-auditing       │
                    │ discriminating-proof    │
                    │ authorization-surface   │
                    │ parser-differential     │
                    │ oracle-driven-fuzzing   │
                    │ assume-breach-modeling  │
                    │ purple-team-exercise    │
                    │ detection-engineering   │
                    │ falsifiable-testing     │
                    │ remediation-reporting   │
                    └────────────┬────────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             ▼                   ▼                   ▼
       INTEGRITY            TRUST / DATA          EVIDENCE
       deterministic       validate-boundary      provenance
       audit-chain         honest-degradation     timeline
       atomic mutation     secret lifecycle       logging
       schema evolution    dependency provenance  decision records
                           resource exhaustion
             │                   │                   │
             └───────────────────┼───────────────────┘
                                 ▼
                       CONSTRUCTION / CHANGE
                                 │
                  secure-by-construction
                  surgical-patcher
                  audit-before-patch
                  git-discipline
                  irreversible-action-gate

                    MACHINE LEARNING
                    (the same discipline, where the
                     test is a metric and the data
                     is the program)

                  data-leakage-hunting
                  training-run-provenance
                  model-evaluation-discipline

                  
---

# SKILLS — Conjunto de Skills de Disciplina de Ingeniería

Una colección de 46 skills para Claude Code que codifican ingeniería de software disciplinada, razonamiento forense y construcción orientada a seguridad. Cada skill se activa automáticamente cuando la conversación coincide con sus condiciones de trigger, inyectando metodología sin que el usuario tenga que pedirla.

Estas skills forman un sistema coherente construido sobre la semiótica triádica de Charles Sanders Peirce y el bucle de inferencia abductiva (abducción → deducción → inducción). Cubren el ciclo de vida completo de ingeniería: investigación, construcción, parcheo, pruebas, auditoría y hardening.

---

## Skills

| # | Skill | Categoría | Se activa cuando |
|---:|---|---|---|
| 1 | `abductive-engineering` | Razonamiento central | Debugging, análisis de causa raíz, respuesta a incidentes, o decisiones arquitectónicas bajo incertidumbre. |
| 2 | `red-team-auditing` | Razonamiento central | Auditorías de seguridad, revisión adversarial, modelado de amenazas, o análisis de invariantes. |
| 3 | `secure-by-construction` | Razonamiento central | Escribir, extender, refactorizar o revisar código con límites de seguridad. |
| 4 | `software-archaeology` | Razonamiento central | Modificar código legado, heredado o desconocido sin romper su comportamiento. |
| 5 | `diagnosing-bugs` | Razonamiento central | Investigar bugs difíciles y regresiones de rendimiento mediante probes controlados y tests de regresión. |
| 6 | `codebase-health-assessment` | Razonamiento central | Clasificar módulos muertos, fósiles, vivos y fuera de alcance antes de modificar un codebase. |
| 7 | `reverse-engineering` | Razonamiento central | Reconstruir sistemas no documentados, binarios, protocolos, formatos de archivo o APIs opacas sin fuente legible. |
| 8 | `daubert-defensible-writing` | Razonamiento central | Escribir hallazgos y reportes que separen evidencia, inferencia, incertidumbre y opinión. |
| 9 | `deterministic-core` | Determinismo e integridad | Producir decisiones reproducibles bit-a-bit y resistentes a manipulación con serialización canónica y sellado SHA-256. |
| 10 | `llm-out-of-the-loop` | Determinismo e integridad | Mantener las decisiones consecuentes fuera del camino del LLM, sellando resultados antes de la narración opcional. |
| 11 | `tamper-evident-audit-chain` | Determinismo e integridad | Construir o verificar logs append-only que detecten alteración, inserción, reordenamiento o eliminación. |
| 12 | `atomic-state-mutation` | Determinismo e integridad | Hacer que operaciones de múltiples escrituras a estado persistente sean todo-o-nada y aisladas de callers concurrentes. |
| 13 | `versioned-schema-evolution` | Determinismo e integridad | Evolucionar artefactos serializados con versiones de esquema explícitas sin romper datos existentes. |
| 14 | `surgical-patcher` | Parcheo y edición | Aplicar cambios anclados, verificados y reversibles en lugar de reescribir archivos fuente completos. |
| 15 | `audit-before-patch` | Parcheo y edición | Validar un hallazgo de auditoría contra el archivo actual antes de cambiar cualquier código. |
| 16 | `validate-at-the-boundary` | Input y datos | Validar input no confiable en el borde del sistema con errores claros. |
| 17 | `honest-degradation` | Input y datos | Manejar input degradado, legado, reconstruido o no verificable sin devolver resultados incorrectos que parecen plausibles. |
| 18 | `sql-aggregation-not-materialization` | Input y datos | Empujar conteos, sumas y agrupaciones a la base de datos en lugar de cargar filas en memoria. |
| 19 | `git-discipline` | Proceso | Mantener las sesiones de coding asistidas por IA recuperables, revisables y libres de reescritura insegura de historia. |
| 20 | `claim-provenance-discipline` | Gobernanza de evidencia | Preservar el origen, nivel epistémico, alcance y falsificador de cada afirmación a través de resúmenes y handoffs. |
| 21 | `attack-surface-triage` | Validación adversarial | Enumerar la superficie de un objetivo autorizado en una cola de candidatos reproducible y falsable — antes de cualquier payload. |
| 22 | `purple-team-exercise` | Validación adversarial | Convertir cada técnica en una hipótesis de detección, detonarla mínima y marcada, y medir qué vio el lado azul. |
| 23 | `detection-engineering` | Validación adversarial | Convertir un requisito de detección en una regla testeada, presupuestada y versionada — con un gemelo benigno que no debe disparar. |
| 24 | `agent-trust-boundaries` | Arquitectura de agentes | Mantener el contenido recuperado como dato, la autoridad de herramientas en política determinística, y romper la tríada no-confiable/datos-privados/salida externa. |
| 25 | `falsifiable-testing` | Verificación | Escribir tests que realmente puedan fallar — rojo primero, controles negativos, fuerza del oráculo, y flakes tratados como hallazgos. |
| 26 | `incident-timeline-reconstruction` | Gobernanza de evidencia | Ordenar eventos entre dominios de reloj, separar tiempo registrado de tiempo real, y etiquetar cada hueco por tipo. |
| 27 | `irreversible-action-gate` | Proceso | Clasificar acciones por reversibilidad y radio de impacto, y compuertarlas con preview, aserción de conteo y plan de deshacer escrito. |
| 28 | `dependency-provenance` | Cadena de suministro | Saber qué se despacha realmente, establecer la identidad del paquete antes que la confianza, y tratar los advisories como candidatos hasta demostrar alcanzabilidad. |
| 29 | `secret-lifecycle-discipline` | Credenciales | Tratar las credenciales como un ciclo de vida — redacción en el borde, rotación ensayada antes de necesitarla, rotar primero ante exposición. |
| 30 | `decision-record-discipline` | Proceso | Capturar fuerzas, alternativas rechazadas, supuestos que sostienen la decisión y disparadores de revisión mientras el contexto todavía existe. |
| 31 | `concurrency-reasoning` | Razonamiento central | Razonar sobre estado mutable compartido, invariantes y orden happens-before en vez de agregar un lock y confiar. |
| 32 | `forensic-logging-design` | Gobernanza de evidencia | Decidir qué registrar hoy para que la reconstrucción de mañana sea posible — decisiones, correlación y silencio legible. |
| 33 | `invariant-hunting` | Razonamiento central | Cazar violaciones de una invariante de seguridad declarada o implícita a través de una transición — una propiedad establecida en T0 que un cambio de estado posterior debe preservar. |
| 34 | `beyond-the-sink` | Razonamiento central | Una investigación se estanca — mirar más allá de la lista de keywords de sink-grep, la familia de preguntas agotada o una sola implementación cuando la capa obvia está seca. |
| 35 | `discriminating-proof` | Verificación | Convertir una hipótesis plausible en un veredicto ganado con el experimento más barato que pueda matarla — oráculo binario, valor canario, control negativo. |
| 36 | `forensic-persistence` | Razonamiento central | Una sesión de hunt, auditoría o debug devuelve cero hallazgos, las hipótesis se refutan una tras otra, o un objetivo parece demasiado endurecido para seguir. |
| 37 | `oracle-driven-fuzzing` | Verificación | Los bugs deben encontrarse con input generado — oráculos property-based, structure-aware, diferenciales y metamórficos, disciplina de corpus, shrinking y triage de crashes. |
| 38 | `parser-differential-hunting` | Validación adversarial | Dos componentes leen los mismos bytes y no coinciden — el checkpoint decide sobre un significado mientras el sink actúa sobre otro. |
| 39 | `authorization-surface-mapping` | Validación adversarial | Construir la matriz actor × recurso × acción y probar las celdas para las que nadie escribió un test — porque un check ausente no se ve. |
| 40 | `assume-breach-modeling` | Validación adversarial | Una posición ya está tomada — mapear qué alcanza esa identidad y encontrar el cuello de botella cuya eliminación corta más caminos. |
| 41 | `resource-exhaustion-review` | Input y datos | Un input pequeño compra una cantidad enorme de trabajo o memoria — ratios de asimetría, asignación no acotada, algoritmos superlineales, falta de backpressure. |
| 42 | `remediation-driven-reporting` | Validación adversarial | Escribir el reporte para que se arregle la clase, no la instancia — sobrevivir al triage, severidad ajustada al impacto demostrado, y verificar el parche contra la clase. |
| 43 | `finding-custody` | Gobernanza de evidencia | Un hallazgo confirmado después de reportarlo — instancia vs clase vs método, la ventana de patch-diffing, custodia del PoC, y una decisión de divulgación con disparador de revisión. |
| 44 | `data-leakage-hunting` | Machine learning | La única clase de bug cuyo síntoma es una mejor métrica — datos de evaluación que llegan al modelo por preprocesamiento, tiempo, grupos, duplicados o un test set gastado. |
| 45 | `training-run-provenance` | Machine learning | Determinismo donde sí es alcanzable — el artefacto, no el proceso: manifiesto sellado, no-determinismo nombrado, y una afirmación de reproducibilidad al escalón que la evidencia sostiene. |
| 46 | `model-evaluation-discipline` | Machine learning | Una evaluación que realmente puede fallar — baseline obligatorio, intervalo en vez de estimación puntual, peor slice en vez de media, y controles negativos. |

### Bucle de validación adversarial

`attack-surface-triage` abre el bucle y `red-team-auditing` es el paso de
confirmación; las skills de caza alimentan candidatos, y las de impacto y
contención devuelven el hallazgo confirmado al lado azul:

```
                 attack-surface-triage → candidatos rankeados
                              │
   ┌──────────────────────────┼──────────────────────────┐
   │  de dónde salen los candidatos (la caza)            │
   │  invariant-hunting · parser-differential-hunting    │
   │  authorization-surface-mapping · beyond-the-sink    │
   │  oracle-driven-fuzzing · resource-exhaustion-review │
   └──────────────────────────┼──────────────────────────┘
                              ▼
      discriminating-proof → red-team-auditing → confirmado / refutado
                              │                        │
                              │        forensic-persistence (refutado → otro eje)
                              ▼
      assume-breach-modeling → impacto, cuellos de botella, contención
                              ▼
      purple-team-exercise → gaps de detección
                              ▼
      detection-engineering → regla probada → (el retest cierra el bucle)

   cuando el objetivo es de otro:
      remediation-driven-reporting → se arregla la clase, no la instancia
      finding-custody → lo que NO dijiste, y qué reabre la decisión
```

Todo lo que en esta biblioteca está del lado ofensivo existe para producir un
artefacto defensivo: un límite, un mamparo, un test negativo generado, o una
regla que disparó por el motivo correcto.

### La costura de machine learning

ML rompe tres supuestos sobre los que se apoya el resto de la biblioteca: el
test es una métrica y no un pass/fail, los datos son el programa real, y la
clase de bug de mayor severidad *sube* la métrica. Las skills 44–46 los
restauran, y se encuentran con `deterministic-core` en un límite preciso:

```
corrida de entren.  →   artefacto congelado →  inferencia  →   decisión
no determinista         hasheado, inmutable    determinista    exacta
training-run-           la costura             mismo artefacto deterministic-core
provenance                                     + input         aplica sin cambios
       ↑                                            ↑
data-leakage-hunting                    model-evaluation-discipline
(¿el número es real?)                   (¿el número es una medición?)
```

El determinismo no deja de ser alcanzable en ML — deja de serlo *aguas arriba
del artefacto*. Todo lo que está aguas abajo se sostiene al mismo estándar que
cualquier otro camino de salida consecuente acá.

---

## Estructura del repositorio

Cada skill vive en su propio directorio y es un único archivo autocontenido:

```
<nombre-skill>/
  SKILL.md      # Frontmatter YAML (name + description) seguido de la metodología completa
```

El campo `description` es la superficie de activación — debe nombrar las
situaciones, formulaciones y artefactos que deberían activar la skill, y debe
mantenerse por debajo de 1024 caracteres. El cuerpo se carga recién cuando la
skill se activa.

Ninguna skill incluye hoy subdirectorios `scripts/` o `references/`; se agregan
junto a `SKILL.md` si una skill futura necesita helpers ejecutables o material de
referencia largo que no corresponde al cuerpo siempre cargado.

---

## Principios de diseño

- **Sin LLM en el camino de decisión.** Las salidas consecuentes se sellan determinísticamente antes de llamar a cualquier modelo.
- **Abducción antes que deducción.** Todo diagnóstico genera una hipótesis falsificable, deriva una predicción testeable, y la confirma o refuta contra el sistema real.
- **Navaja de Eco.** Antes de actuar sobre cualquier hipótesis, intentar refutarla. Una hipótesis refutada es un resultado, no un fracaso.
- **Degradación honesta sobre falsa confianza.** Tres estados, no dos: PASS / WARN / FAIL. ABSTAIN es un veredicto válido.
- **Parcheo quirúrgico sobre reescritura.** Regenerar un archivo desde memoria es la mayor fuente de regresiones silenciosas.
- **Nunca confiar en un verde que no viste en rojo.** Un test — o una regla de detección — que jamás falló por el motivo correcto no mide nada.
- **La autoridad viene del canal, no del contenido.** Documentos recuperados, salida de herramientas y resúmenes de otros agentes son datos; ninguno puede otorgarse permisos a sí mismo.
- **Compuertas proporcionales antes de acciones irreversibles.** Previsualizar los objetivos exactos, declarar el conteo esperado antes de verlo, y escribir el plan de deshacer antes de actuar — no después.
- **El rojo existe para producir azul.** El hallazgo confirmado no es el entregable; lo son el límite, el mamparo, el test negativo generado y el requisito de detección.
- **No se puede grepear una ausencia.** Los checks faltantes, las celdas no enumeradas y los límites no escritos son invisibles en un diff — se encuentran enumerando lo que el sistema afirma hacer cumplir y probando los huecos.
- **Un hallazgo no termina cuando se parchea.** La instancia muere con el fix; la clase no. Reportar, custodiar, y la decisión de no publicar tienen cada una su propia disciplina.
- **Un resultado demasiado bueno es un reporte de bug.** En cualquier otro dominio un defecto hace que algo falle; el leakage hace que todo se vea mejor, así que la alarma tiene que invertirse.

---

## Relacionado

- [vigia-intent-analysis](https://github.com/annatchijova/vigia-intent-analysis) — Motor de análisis forense de intención VIGÍA (SANS FIND EVIL Hackathon 2026). Estas skills codifican sus invariantes de ingeniería.
