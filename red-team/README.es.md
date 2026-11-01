# Skills de evaluación Red Team

**Idioma:** Español · [English](README.md)

En seguridad, a veces se pasa de una alerta de scanner o un fragmento sospechoso directamente a un veredicto. Esta colección ayuda al agente a establecer qué ocurrió, contrastar explicaciones alternativas y dejar evidencia reproducible antes de recomendar un cambio.

Combina procedimientos de evaluación específicos por dominio con las metodologías de ingeniería de la colección `SKILLS` principal. Está pensada para revisiones autorizadas de repositorios, fixtures sintéticos y trabajo en laboratorios controlados. Cada procedimiento indica qué evidencia respaldaría o refutaría una hipótesis y distingue los casos no probados de los resultados obtenidos.

**Inventario:** 79 skills de dominio reescritas a partir de Claude-Red y 28 copias sin modificar de metodologías locales. La colección principal completa tiene 92 skills; esta subcolección tiene 107.

**Por dónde empezar:** [Elegir y cargar skills](#elegir-un-conjunto-de-skills) · [Método de evaluación](METHODOLOGY.md) · [Mapa de las 79 fuentes](COVERAGE.md) · [Registro de validación](VALIDATION.md)

## Elegir un conjunto de skills

Ejecutá uno de estos comandos desde el directorio padre `SKILLS`. El catálogo devuelve nombres, rutas y hashes, sin recorrer subdirectorios:

```bash
python3 -B red-team/catalog.py general
python3 -B red-team/catalog.py red-team
```

Pasale al agente las rutas de un solo resultado y pedile que cargue exclusivamente ese conjunto. El catálogo ayuda a delimitar la selección; la carpeta no cambia la configuración de descubrimiento automático de un agente. Para trabajo general, usá sólo la colección padre y excluí `red-team/` y sus descendientes. Para una sesión red team, usá sólo el resultado del catálogo red-team.

Instrucción sugerida: “Usá únicamente las rutas devueltas por el catálogo red-team. Leé los SKILL.md pertinentes y METHODOLOGY.md antes de actuar. No cargues skills de la colección padre.”

## Contenido

Las 79 evaluaciones de dominio cubren seguridad de aplicaciones y APIs, autenticación, identidad cloud y CI/CD, cadena de suministro, contenedores y Kubernetes, criptografía, fuzzing y análisis de binarios, redes inalámbricas y sistemas embebidos, móviles, OSINT, ingeniería social, Active Directory, visibilidad de endpoints y evidencia de postexplotación. [COVERAGE.md](COVERAGE.md) enumera cada fuente, destino, mecanismo conservado y motivo de adaptación.

Las 28 copias de skills locales aportan métodos comunes de autorización, hipótesis, evidencia, reporting y detección. Las seis skills de dominio que existían antes de la expansión conservan sus nombres; las demás adaptaciones usan el prefijo `rt-`. Elegí sólo los procedimientos pertinentes para la pregunta actual.

## Cómo usar un procedimiento

Empezá por [METHODOLOGY.md](METHODOLOGY.md) y después leé la skill elegida. Describe el mecanismo del dominio, la línea de base y la explicación alternativa, un experimento acotado, sus controles, la evidencia que hay que conservar y cómo interpretar el resultado. Los casos de aceptación incluidos describen decisiones esperadas frente a cierta evidencia; no afirman que se hayan probado sistemas reales. La disponibilidad de herramientas y sus comportamientos según versión se deben comprobar en el entorno concreto.

El catálogo sirve para seleccionar, no es una frontera de aislamiento. El texto de las copias puede mencionar skills relacionadas. Si una referencia no está en el conjunto elegido, seguí sólo si el procedimiento sigue siendo autónomo; de lo contrario, explicitá la limitación en vez de cargar otra colección sin indicarlo.

## Procedencia y verificación

Las skills de dominio se adaptaron desde Claude-Red, revisión `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Las carpetas de metodologías locales son copias, no enlaces simbólicos. [PROVENANCE.md](PROVENANCE.md) explica la selección y adaptación; [VALIDATION.md](VALIDATION.md) registra las comprobaciones estructurales, la revisión independiente y sus límites. Actualizá las copias de manera deliberada y revisá el diff; no sincronices automáticamente sobre cambios locales.

Para repetir las comprobaciones registradas desde el directorio padre `SKILLS`:

```bash
python3 -B -m unittest -v red-team/test_collection.py
python3 -B red-team/validate_collection.py --upstream /path/to/Claude-Red
```
