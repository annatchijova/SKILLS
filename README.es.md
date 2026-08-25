# SKILLS — Conjunto de Skills de Disciplina de Ingeniería

**Idioma:** [English](README.md) · Español

Una colección de 53 skills para Claude Code que codifican ingeniería de software disciplinada, razonamiento forense y construcción orientada a seguridad. Cada skill se activa automáticamente cuando la conversación coincide con sus condiciones de trigger, inyectando metodología sin que el usuario tenga que pedirla.

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
| 47 | `training-serving-parity` | Machine learning | Las features con las que se entrenó un modelo no son las que se le sirven — dos implementaciones de un mismo cálculo, y el default silencioso que responde con confianza sobre un vector nunca visto. |
| 48 | `beyond-the-fix` | Razonamiento central | Auditar las correcciones mismas — un parche prueba que alguien supo que ahí había algo mal, nunca que ahora esté bien; ocho formas en que un fix se queda corto, y el control pre-fix que las distingue. |
| 49 | `dual-use-behavior-adjudication` | Operaciones de seguridad | Decidir malicioso vs benigno cuando la herramienta misma es legítima — el problema del living-off-the-land, donde el veredicto vive en la procedencia, el baseline y la secuencia, nunca en el artefacto. |
| 50 | `threat-attribution-restraint` | Operaciones de seguridad | Resistir la pulsión de nombrar un actor — todo solape que apunta a APT-X es contacto entre datasets, no identidad de manos, y casi todo es barato de plantar. |
| 51 | `credential-material-triage` | Credenciales | Convertir "encontramos una credencial" en un hallazgo — como qué autentica, qué autoriza, por cuánto tiempo y cómo se revoca, sin inflar un hash en un compromiso. |
| 52 | `cloud-control-plane-reasoning` | Operaciones de seguridad | Razonar el compromiso cloud sobre el grafo de identidad y control-plane, no el diagrama de red — donde una key robada está a un AssumeRole de toda la cuenta. |
| 53 | `untrusted-sample-handling` | Operaciones de seguridad | Examinar un artefacto hostil de forma segura — nunca dejarlo ejecutar donde alcance algo real, nunca confundir lo que puede hacer con aquello a lo que apuntaba. |

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
   │  beyond-the-fix (the fix history is the map)        │
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
clase de bug de mayor severidad *sube* la métrica. Las skills 44–47 los
restauran, y se encuentran con `deterministic-core` en un límite preciso:

```
corrida de entren.  →   artefacto congelado →  inferencia  →   decisión
no determinista         hasheado, inmutable    determinista    exacta
training-run-           la costura             mismo artefacto deterministic-core
provenance                                     + input         aplica sin cambios
       ↑                        ↑                   ↑
data-leakage-hunting   training-serving-parity   model-evaluation-discipline
(¿el número es real?)  (¿el input servido es     (¿el número es una
                        el input entrenado?)      medición?)
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
- **Un fix prueba el pasado, no el presente.** Que alguien lo haya arreglado significa que arregló eso y nada más — el archivo parcheado es el código menos revisado del repo y el lugar más probable del próximo bug.

---

## Relacionado

- [vigia-intent-analysis](https://github.com/annatchijova/vigia-intent-analysis) — Motor de análisis forense de intención VIGÍA (SANS FIND EVIL Hackathon 2026). Estas skills codifican sus invariantes de ingeniería.
