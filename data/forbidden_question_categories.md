# Taxonomía de categorías prohibidas (forbidden_question)

Estas son las **13 categorías** de contenido prohibido usadas por el dataset
[`verazuo/jailbreak_llms`](https://github.com/verazuo/jailbreak_llms)
(`data/forbidden_question/forbidden_question_set.csv`). Son **solo etiquetas de clasificación**,
no contienen prompts ni payloads.

Se usan en ALUCINAJE para **etiquetar y agrupar casos de prueba** y para medir la robustez por categoría
(p. ej. tasa de rechazo correcto por tipo de contenido). Ver [`docs/DATA_SOURCES.md`](../docs/DATA_SOURCES.md).

| # | Categoría (EN) | Descripción breve |
|---|----------------|-------------------|
| 1 | Illegal Activity | Actividades ilegales en general |
| 2 | Hate Speech | Discurso de odio / discriminación |
| 3 | Malware | Generación de software malicioso |
| 4 | Physical Harm | Daño físico a personas |
| 5 | Economic Harm | Daño económico |
| 6 | Fraud | Fraude y engaño |
| 7 | Pornography | Contenido sexual explícito |
| 8 | Political Lobbying | Campañas / lobby político |
| 9 | Privacy Violence | Violación de la privacidad |
| 10 | Legal Opinion | Asesoramiento legal no cualificado |
| 11 | Financial Advice | Asesoramiento financiero no cualificado |
| 12 | Health Consultation | Consulta médica no cualificada |
| 13 | Gov Decision | Decisiones de gobierno / administración |

Fuente y licencia: `verazuo/jailbreak_llms` (MIT). Atribución en [`docs/DATA_SOURCES.md`](../docs/DATA_SOURCES.md).
