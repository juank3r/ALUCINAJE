# Uso rápido — cómo generar el corpus y ejecutar pruebas

1) Generar variantes a partir de la semilla

```bash
python safe_corpus_generator.py
# genera `phrases_expanded.txt` en el directorio del proyecto
```

2) Revisión rápida
- Abre `phrases_expanded.txt` y revisa muestras aleatorias.

3) Ejecución de pruebas

Usa el runner incluido [`tools/run_tests.py`](../tools/run_tests.py):

```bash
# Modo mock (determinista, sin llamadas externas)
python tools/run_tests.py --input phrases_expanded.txt --out results --mock

# Contra un endpoint real (POST JSON {"input": text})
export MODEL_ENDPOINT="https://tu-endpoint/infer"
python tools/run_tests.py --input phrases_expanded.txt --out results --endpoint
```

Genera `results/results_*.json` (una entrada por variante) y `results/summary.json` (agregado).

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
