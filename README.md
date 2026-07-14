# SKILLS — Engineering Discipline Skill Set

A collection of 19 skills for Claude Code that encode disciplined software engineering, forensic reasoning, and security-first construction. Each skill activates automatically when the conversation matches its trigger conditions, injecting methodology without requiring the user to ask for it.

These skills form a coherent system built on Charles Sanders Peirce's triadic semiotics and the abductive inference loop (abduction → deduction → induction). They cover the full engineering lifecycle: investigation, construction, patching, testing, auditing, and hardening.

---

## Skills

### Core Reasoning

| Skill | Activates when |
|-------|---------------|
| **abductive-engineering** | Debugging, root cause analysis, incident response, architectural decisions under uncertainty, or any request for a rigorous hypothesis-driven approach. |
| **red-team-auditing** | Security audits, adversarial review, threat modeling, finding vulnerabilities or invariant violations, or auditing another agent's audit. |
| **secure-by-construction** | Writing, extending, refactoring, or reviewing code — features, APIs, parsers, auth, schemas, tests. Especially when the user asks for speed. |
| **software-archaeology** | Modifying legacy, inherited, or unfamiliar code — change without breakage, deletion without data loss, understanding before editing. |
| **diagnosing-bugs** | Hard bugs and performance regressions — build a tight feedback loop before forming any hypothesis, rank 3-5 alternatives, instrument one variable at a time, tag every probe, write the regression test before the fix. Operational mechanics companion to abductive-engineering. |
| **codebase-health-assessment** | Auditing a codebase for dead, fossil, and live modules — classify every file before acting, apply the deletion test, produce a structured filterable report. Triage nurse to software-archaeology's surgeon. |
| **reverse-engineering** | Reconstructing how an undocumented, closed, or unfamiliar system works when you do NOT have its source — binaries, protocols, file formats, opaque APIs, firmware, memory dumps. Sibling of software-archaeology: use this one when you lack readable source. |
| **daubert-defensible-writing** | Writing reports, findings, documentation, or any prose that asserts conclusions — separating fact from inference, admitting uncertainty without weakening the conclusion, never overclaiming under persuasion pressure. |

### Determinism and Integrity

| Skill | Activates when |
|-------|---------------|
| **deterministic-core** | Any output path that must be reproducible bit-for-bit and tamper-evident: no floats in the decision path, canonical serialization, SHA-256 sealing. |
| **llm-out-of-the-loop** | Designing systems with consequential outputs — the LLM stays out of the decision path; results are sealed before the model is called. |
| **tamper-evident-audit-chain** | Building or verifying append-only logs that prove no entry was altered, inserted, reordered, or dropped after the fact. |
| **atomic-state-mutation** | Any logical operation spanning several writes to persistent state that must land all-or-nothing, isolated from concurrent callers. |
| **versioned-schema-evolution** | Stamping serialized artifacts with a schema version and evolving the format without breaking existing data. |

### Patching and Editing

| Skill | Activates when |
|-------|---------------|
| **surgical-patcher** | Applying changes to existing source files — anchored, verified, reversible patches instead of rewriting whole files. |
| **audit-before-patch** | Validating any audit finding, bug report, or proposed fix against the actual current file content before changing a single line. |

### Input and Data

| Skill | Activates when |
|-------|---------------|
| **validate-at-the-boundary** | Handling untrusted inputs — validate at the edge of the system with a clear error at the boundary, not deep inside. |
| **honest-degradation** | Code running on degraded, legacy, reconstructed, or unverifiable input — fail visibly instead of returning a plausible-looking wrong answer. |
| **sql-aggregation-not-materialization** | Counting, summing, or grouping data — push the aggregation into the database instead of loading rows into application memory. |

### Process

| Skill | Activates when |
|-------|---------------|
| **git-discipline** | AI-assisted or agentic coding sessions — tag a restore point, forbid rebase/force-push, verify state before claiming it. |

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

Una colección de 19 skills para Claude Code que codifican ingeniería de software disciplinada, razonamiento forense y construcción orientada a seguridad. Cada skill se activa automáticamente cuando la conversación coincide con sus condiciones de trigger, inyectando metodología sin que el usuario tenga que pedirla.

Estas skills forman un sistema coherente construido sobre la semiótica triádica de Charles Sanders Peirce y el bucle de inferencia abductiva (abducción → deducción → inducción). Cubren el ciclo de vida completo de ingeniería: investigación, construcción, parcheo, pruebas, auditoría y hardening.

---

## Skills

### Razonamiento central

| Skill | Se activa cuando |
|-------|-----------------|
| **abductive-engineering** | Debugging, análisis de causa raíz, respuesta a incidentes, decisiones arquitectónicas bajo incertidumbre, o cualquier pedido de un enfoque riguroso basado en hipótesis. |
| **red-team-auditing** | Auditorías de seguridad, revisión adversarial, modelado de amenazas, búsqueda de vulnerabilidades o violaciones de invariantes, o auditar la auditoría de otro agente. |
| **secure-by-construction** | Escribir, extender, refactorizar o revisar código — features, APIs, parsers, auth, esquemas, tests. Especialmente cuando el usuario pide velocidad. |
| **software-archaeology** | Modificar código legado, heredado o desconocido — cambiar sin romper, borrar sin perder datos, entender antes de editar. |
| **diagnosing-bugs** | Bugs difíciles y regresiones de rendimiento — construir un loop de feedback antes de formular hipótesis, rankear 3-5 alternativas, instrumentar una variable a la vez, taggear cada probe, escribir el test de regresión antes del fix. Mecánica operacional compañera de abductive-engineering. |
| **codebase-health-assessment** | Auditar un codebase para encontrar módulos muertos, fósiles y vivos — clasificar cada archivo antes de actuar, aplicar el deletion test, producir un reporte estructurado y filtrable. Enfermera de triage a la cirujana software-archaeology. |
| **reverse-engineering** | Reconstruir cómo funciona un sistema no documentado, cerrado o desconocido cuando NO se tiene el código fuente — binarios, protocolos, formatos de archivo, APIs opacas, firmware, dumps de memoria. Hermana de software-archaeology: usar esta cuando no hay fuente legible. |
| **daubert-defensible-writing** | Escribir reportes, hallazgos, documentación o cualquier prosa que afirma conclusiones — separando hecho de inferencia, admitiendo incertidumbre sin debilitar la conclusión, sin sobreclamar bajo presión de persuasión. |

### Determinismo e integridad

| Skill | Se activa cuando |
|-------|-----------------|
| **deterministic-core** | Cualquier camino de salida que deba ser reproducible bit-a-bit y resistente a manipulación: sin floats en el camino de decisión, serialización canónica, sellado con SHA-256. |
| **llm-out-of-the-loop** | Diseñar sistemas con salidas consecuentes — el LLM queda fuera del camino de decisión; los resultados se sellan antes de llamar al modelo. |
| **tamper-evident-audit-chain** | Construir o verificar logs append-only que prueben que ninguna entrada fue alterada, insertada, reordenada o eliminada después del hecho. |
| **atomic-state-mutation** | Cualquier operación lógica que abarque varias escrituras a estado persistente y deba ejecutarse toda o ninguna, aislada de callers concurrentes. |
| **versioned-schema-evolution** | Estampar artefactos serializados con una versión de esquema y evolucionar el formato sin romper datos existentes. |

### Parcheo y edición

| Skill | Se activa cuando |
|-------|-----------------|
| **surgical-patcher** | Aplicar cambios a archivos fuente existentes — patches anclados, verificados y reversibles, en lugar de reescribir archivos completos. |
| **audit-before-patch** | Validar cualquier hallazgo de auditoría, reporte de bug o fix propuesto contra el contenido real y actual del archivo antes de cambiar una sola línea. |

### Input y datos

| Skill | Se activa cuando |
|-------|-----------------|
| **validate-at-the-boundary** | Manejar inputs no confiables — validar en el borde del sistema con un error claro en la frontera, no en las profundidades del código. |
| **honest-degradation** | Código que corre sobre input degradado, legado, reconstruido o no verificable — fallar visiblemente en lugar de devolver una respuesta incorrecta que parece plausible. |
| **sql-aggregation-not-materialization** | Contar, sumar o agrupar datos — empujar la agregación a la base de datos en lugar de cargar filas en memoria de la aplicación. |

### Proceso

| Skill | Se activa cuando |
|-------|-----------------|
| **git-discipline** | Sesiones de coding asistidas por IA o agénticas — taggear un punto de restauración, prohibir rebase/force-push, verificar el estado antes de declararlo. |

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
