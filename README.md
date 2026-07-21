# SKILLS — Engineering Discipline Skill Set

A collection of 20 skills for Claude Code that encode disciplined software engineering, forensic reasoning, and security-first construction. Each skill activates automatically when the conversation matches its trigger conditions, injecting methodology without requiring the user to ask for it.

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

---

## Repository Structure

Each skill lives in its own directory:

```
<skill-name>/
  SKILL.md                        # Frontmatter + full methodology
  <skill-name>.trigger.json       # Evaluation corpus: queries that should/should not trigger
  scripts/                        # Helper scripts referenced by the skill (where applicable)
  references/                     # Supporting reference documents (where applicable)
```

---

## Design Principles

- **No LLM in the decision path.** Consequential outputs are sealed deterministically before any model is called.
- **Abduction before deduction.** Every diagnosis generates a falsifiable hypothesis, derives a testable prediction, and confirms or refutes it against the real system.
- **Eco's razor.** Before acting on any hypothesis, attempt to refute it. A refuted hypothesis is a result, not a failure.
- **Honest degradation over false confidence.** Three states, not two: PASS / WARN / FAIL. ABSTAIN is a valid verdict.
- **Surgical patching over rewriting.** Regenerating a file from memory is the largest source of silent regressions.

---

## Related

- [vigia-intent-analysis](https://github.com/annatchijova/vigia-intent-analysis) — VIGÍA forensic intent analysis engine (SANS FIND EVIL Hackathon 2026). These skills encode its engineering invariants.

---

---

# SKILLS — Conjunto de Skills de Disciplina de Ingeniería

Una colección de 20 skills para Claude Code que codifican ingeniería de software disciplinada, razonamiento forense y construcción orientada a seguridad. Cada skill se activa automáticamente cuando la conversación coincide con sus condiciones de trigger, inyectando metodología sin que el usuario tenga que pedirla.

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

---

## Estructura del repositorio

Cada skill vive en su propio directorio:

```
<nombre-skill>/
  SKILL.md                        # Frontmatter + metodología completa
  <nombre-skill>.trigger.json     # Corpus de evaluación: queries que deben/no deben triggerear
  scripts/                        # Scripts de apoyo referenciados por la skill (donde aplica)
  references/                     # Documentos de referencia (donde aplica)
```

---

## Principios de diseño

- **Sin LLM en el camino de decisión.** Las salidas consecuentes se sellan determinísticamente antes de llamar a cualquier modelo.
- **Abducción antes que deducción.** Todo diagnóstico genera una hipótesis falsificable, deriva una predicción testeable, y la confirma o refuta contra el sistema real.
- **Navaja de Eco.** Antes de actuar sobre cualquier hipótesis, intentar refutarla. Una hipótesis refutada es un resultado, no un fracaso.
- **Degradación honesta sobre falsa confianza.** Tres estados, no dos: PASS / WARN / FAIL. ABSTAIN es un veredicto válido.
- **Parcheo quirúrgico sobre reescritura.** Regenerar un archivo desde memoria es la mayor fuente de regresiones silenciosas.

---

## Relacionado

- [vigia-intent-analysis](https://github.com/annatchijova/vigia-intent-analysis) — Motor de análisis forense de intención VIGÍA (SANS FIND EVIL Hackathon 2026). Estas skills codifican sus invariantes de ingeniería.
