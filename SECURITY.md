# Política de seguridad

ALUCINAJE es un proyecto **defensivo** de medición de robustez de LLMs. Esta política cubre la
divulgación responsable de problemas de seguridad del propio proyecto (no de modelos de terceros).

## Alcance

- Fallos en el filtrado/saneado que permitan que contenido inseguro entre en el corpus.
- Fugas de datos sensibles (PII, credenciales) en corpora, artefactos o métricas.
- Problemas en el harness de evaluación (p. ej. que persista payloads que deberían ser efímeros).

## Cómo reportar

Abre un aviso privado con **GitHub Security Advisories** en el repositorio, o un issue con la etiqueta
`security` **sin** incluir contenido sensible/operativo. Incluye pasos de reproducción y el impacto.

## Compromisos

- Confirmación de recepción y triage razonable.
- Corrección priorizada según severidad; plan de mitigación (bloqueo, rotación de credenciales,
  notificación a stakeholders) según [`docs/JAILBREAK_RISKS.md`](docs/JAILBREAK_RISKS.md).

## Hallazgos conocidos

- El filtro `is_probably_jailbreak()` es **léxico** (palabras clave), no semántico: puede dejar pasar
  jailbreaks parafraseados. Mitigación vigente: nada del import se commitea automáticamente y
  `phrases_seed.txt` se mantiene curado a mano. Detalle en [`docs/FILTERING.md`](docs/FILTERING.md).
