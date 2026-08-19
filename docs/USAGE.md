# Uso rápido — cómo generar el corpus y ejecutar pruebas

1) Generar variantes a partir de la semilla

```bash
python safe_corpus_generator.py
# genera `phrases_expanded.txt` en el directorio del proyecto
```

2) Revisión rápida
- Abre `phrases_expanded.txt` y revisa muestras aleatorias.

3) Ejecución de pruebas (esqueleto)
- Implementa un runner que lea cada línea de `phrases_expanded.txt`, llame al endpoint del modelo y guarde respuestas en JSON.

Formato mínimo de output (JSON por entrada):

{
  "input_id": "uuid",
  "variant": "texto de entrada",
  "response": "texto respuesta",
  "status": "ok|rejected|timeout",
  "latency_ms": 123,
}

4) Evaluación
- Usa `docs/PIPELINE.md` para entender métricas y generar `metrics/*.csv`.
