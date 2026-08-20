Metodología para pruebas de robustez de LLMs (ALUCINAJE)

Objetivo:
- Proporcionar un marco responsable para evaluar la robustez y comportamiento de modelos y agentes sin ayudar a evadir controles de seguridad.

Alcance:
- Casos de prueba adversariales seguros (ambigüedad, instrucciones contradictorias, contexto largo, inyección de contexto, fallos de formato).
- No incluye ni generará frases destinadas a "jailbreak" que instruyan a evadir políticas o controles.

Fases de trabajo:
1. Recolección: extraer ejemplos públicos y meta-datos del repositorio objetivo y del sitio (README, issues, ejemplos de uso).
2. Clasificación: etiquetar ejemplos por categoría (ambigüedad, instrucción-confusa, contexto, social-engineering técnico, etc.). Para contenido prohibido, usar la taxonomía de `data/forbidden_question_categories.md`.
3. Generación: crear variaciones seguras por parafraseo, plantillas y fuzzing controlado.
4. Evaluación: ejecutar tests automatizados contra modelos/agents y registrar métricas (respuesta, rechazo, toxicidad, precisión, cumplimiento de políticas).
5. Informe y remediación: resumir hallazgos, clasificar riesgos y proponer mitigaciones.

Tipos de pruebas y ejemplos de métricas:
- Robustez a instrucciones ambiguas: medir tasa de respuestas fuera de política.
- Consistencia: coherencia entre respuestas a variantes de la misma intención.
- Inyección de contexto: verificar que el modelo prioriza instrucciones válidas y recuerda restricciones.
- Métricas: tasa de fallo, tasa de rechazo correcto, cambios semánticos por parafraseo, tiempo de respuesta.

Gobernanza y ética:
- Mantener registros, responsable de pruebas, plan de divulgación responsable para vulnerabilidades.
