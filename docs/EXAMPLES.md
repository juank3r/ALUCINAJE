# Ejemplo trabajado: de la semilla a un informe de robustez

Este documento recorre **un caso de uso completo** de ALUCINAJE, con artefactos y gráficos de ejemplo.
El objetivo: mostrar qué produce el pipeline y cómo se lee el resultado.

> Los números de los gráficos de evaluación son **ilustrativos**. Los reales los genera
> [`tools/eval_jailbreaks.py`](../tools/eval_jailbreaks.py) contra un endpoint (`MODEL_ENDPOINT`).

## 1. Generar el corpus seguro

```bash
python safe_corpus_generator.py --seed phrases_seed.txt --out phrases_expanded.txt --factor 3 --min-len 10
```

`phrases_seed.txt` (9 frases curadas) se expande por parafraseo y permutaciones controladas. Ejemplo de
entrada → variantes seguras:

| Semilla | Variantes generadas (muestra) |
|---|---|
| "Describe cómo evaluar la robustez de un sistema de autenticación." | "Describe de qué manera evaluar la robustez…" · "Por favor, describe cómo evaluar…" · "En resumen: describe cómo evaluar…" |

## 2. Ejecutar las pruebas (mock o endpoint)

```bash
# sin llamadas externas (determinista)
python tools/run_tests.py --input phrases_expanded.txt --out results --mock
```

Salida por entrada (`results/results_*.json`):

```json
{ "input_id": "1", "variant": "Describe cómo evaluar…", "response": "[MOCK] …",
  "status": "ok", "latency_ms": 0 }
```

Y un agregado (`results/summary.json`) con `total`, `unique_inputs`, `errors`, `refusals`,
`refusal_rate`, `avg_latency_ms`.

## 3. Medir robustez frente a jailbreaks reales

Aquí es donde se usa "la web de jailbreak" **de la forma correcta**: como conjunto de evaluación, no como
semilla. Los prompts se descargan en tiempo de test y **no se almacenan**.

```bash
MODEL_ENDPOINT="https://tu-endpoint/infer" python tools/eval_jailbreaks.py --limit 1405 --out metrics
```

### Informe de robustez (ejemplo)

![Informe de robustez de ejemplo](assets/chart-dashboard.svg)

Lectura rápida:
- **Tasa de rechazo 92,4%** — de 1 405 jailbreaks, el modelo rechazó 1 298.
- **Fuga (leak) 6,1%** — 86 respuestas cumplieron total o parcialmente → casos a revisar.
- **Errores 1,5%** — timeouts / respuestas vacías.

### Desglose por categoría

![Tasa de rechazo por categoría](assets/chart-refusal-by-category.svg)

Las categorías de **asesoría** (legal, financiera, salud) son las más débiles. Acción: priorizar
mitigaciones y casos de prueba en esas categorías. Ver taxonomía en
[`data/forbidden_question_categories.md`](../data/forbidden_question_categories.md).

## 4. Por qué NO se minan estos repos para el seed

Al ejecutar el import sobre las fuentes, el saneado deja pasar demasiado:

![Embudo de saneado](assets/chart-funnel.svg)

De 37 332 candidatos el filtro solo descarta 1 779 como jailbreak; lo "conservado" (26 843) incluye guía
operativa y NSFW. Conclusión: `phrases_seed.txt` se mantiene **curado a mano**; los jailbreaks solo se usan
para **evaluar**. Detalle en [`docs/FILTERING.md`](FILTERING.md) y [`docs/DATA_SOURCES.md`](DATA_SOURCES.md).

## 5. Iterar

Con las métricas se ajustan generador y filtros, se añaden casos en las categorías débiles y se repite.
Es el bucle de realimentación del [pipeline](PIPELINE.md).
