# Arquitectura del proyecto ALUCINAJE

![Arquitectura de ALUCINAJE](assets/architecture.svg)

Resumen
- ALUCINAJE está diseñado como una canalización modular para generar corpus adversariales seguros, ejecutar pruebas automatizadas contra modelos/agents y registrar métricas.

Componentes principales
- `Seed Corpus` — archivos de semilla (`phrases_seed.txt`) con entradas humanas supervisadas.
- `Generator` — `safe_corpus_generator.py`: parafraseo, permutaciones y fuzzing controlado.
- `Filters` — reglas automáticas para evitar contenido sensible (filtros de seguridad, listas de palabras prohibidas, detectores de PII).
- `Test Runner` — orquestador que envía variantes al modelo/agent, aplica timeouts y captura respuestas.
- `Evaluator` — módulos que calculan métricas: tasa de rechazo, divergencia semántica, toxicidad, precisión.
- `Human in the Loop` — revisión manual de casos borderline y tuning de filtros.
- `Storage` — versionado de corpora, resultados y trazas para auditoría.

Flujos de datos
- Edición → Seed Corpus → Generator → Candidate Variants → Filters → Test Runner → Results → Evaluator → Human Review → Corpus incrementado

Almacenamiento y reproducibilidad
- Cada ejecución guarda: seed used, generator parameters, version del modelo testeado, y resultados con timestamp.
- Recomendar usar control de versiones (git) y un almacenamiento de artefactos (S3 / Azure Blob / Git LFS según escala).

Seguridad y gobernanza
- No almacenar tokens, credenciales ni datos sensibles en el corpus.
- Mantener registro de accesos, pruebas y responsables.
- Plan de divulgación para vulnerabilidades descubiertas.

Referencias
- Ver `methodology.md` para el flujo operativo y criterios de clasificación.
