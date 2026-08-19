# Consecuencias y riesgos de los "jailbreaks"

Qué es un "jailbreak" (resumen)
- En este contexto, un "jailbreak" se refiere a técnicas que intentan inducir a un modelo a ignorar políticas, revelar información sensible o ejecutar acciones no autorizadas.

Riesgos legales y de cumplimiento
- Divulgación de datos personales o secretos comerciales puede exponer a la empresa a multas, sanciones regulatorias (GDPR, etc.) y reclamaciones legales.

Riesgos reputacionales
- Publicar o permitir que modelos respondan con información dañina puede erosionar la confianza de clientes y socios.

Riesgos de seguridad y operativos
- Filtración de credenciales o rutas de ataque.
- Automatización de actividades maliciosas si el modelo responde con instrucciones operativas.

Riesgos éticos
- Uso indebido por terceros: armas, fraude, desinformación.

Mitigaciones recomendadas
- No incorporar jailbreaks reales en corpora públicos.
- Filtrar y anonimizar datos de prueba.
- Mantener controles de acceso, auditoría y revisión humana para casos borderline.
- Plan de respuesta: bloqueo, rotación de credenciales, notificación a stakeholders.

Nota para testers
- El objetivo de nuestras pruebas es medir resiliencia y fortalecer controles, no producir listas de jailbreaks que circulen públicamente.
