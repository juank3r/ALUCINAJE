# Cómo funciona el filtrado

Este documento explica **qué se descarta y por qué** cuando se importan prompts desde fuentes externas,
para que quede claro qué acaba (y qué NO) en el repositorio.

Todo el filtrado vive en [`tools/import_and_sanitize.py`](../tools/import_and_sanitize.py).

## Flujo de un candidato

```
texto de un fichero .md/.txt/.csv/.json/.yml
        │
        ▼
extract_candidates()   → parte en párrafos, quita code-fences y URLs, longitud 10–600
        │
        ▼
sanitize()             → aplica los filtros de abajo; dedupe
        │
        ├── len < 15 .......................... DESCARTADO (dropped_short)
        ├── is_probably_jailbreak() == True ... DESCARTADO (dropped_jailbreak)
        ├── duplicado ......................... DESCARTADO (dropped_duplicate)
        ▼
frase segura → phrases_imported_sanitized.txt   (+ métricas en .summary.json)
```

## El filtro anti-jailbreak: `is_probably_jailbreak()`

Devuelve `True` (→ se descarta) si el texto, en minúsculas, contiene alguno de estos patrones:

| Patrón | Por qué |
|--------|---------|
| `jailbreak`, `bypass`, `evad*` | intención explícita de evadir controles |
| `ignore (instructions\|safety\|previous)` | anulación de instrucciones del sistema |
| `disable`, `override`, `do not follow` | desactivar salvaguardas |
| `roleplay`, `pretend`, `you are now`, `assistant should` | encuadres típicos de jailbreak |
| `how to (bypass\|disable\|evade)`, `step by step`, `exploit`, `payload` | operativa de ataque |
| `how to`, `tell me how`, `show me how`, `give me steps to` | petición de instrucciones operativas |

> **Diseño conservador (a propósito).** Preferimos **falsos positivos** (descartar de más) antes que dejar
> pasar un jailbreak. Esto implica que frases legítimas que contengan p. ej. `roleplay` o `step by step`
> también se descartan. Es intencionado: el objetivo del import es alimentar un **corpus seguro**, no
> capturar todo.

## Qué significa esto para las fuentes upstream

- De `verazuo/jailbreak_llms`, **los 1.405 prompts de jailbreak se descartan** por este filtro (contienen
  justo esos patrones). Solo pasan frases neutras/regulares. Por eso el import **no** convierte el repo en
  una colección de jailbreaks.
- Los prompts de jailbreak **no se copian** al repo. Si quieres **medir la robustez** de un modelo frente a
  ellos, usa el **modo evaluación** ([`tools/eval_jailbreaks.py`](../tools/eval_jailbreaks.py)), que los usa
  como *entradas de test* en tiempo de ejecución sin guardarlos ni amplificarlos.

## Métricas del filtrado

Cada ejecución de `import_and_sanitize.py` escribe `phrases_imported_sanitized.summary.json`:

```json
{
  "repos": 2,
  "files_scanned": 0,
  "totals": { "candidates": 0, "dropped_short": 0, "dropped_jailbreak": 0,
              "dropped_duplicate": 0, "kept": 0 },
  "repos_detail": [ ... ]
}
```

`dropped_jailbreak` es el nº de candidatos rechazados por `is_probably_jailbreak()`.

## Limitaciones conocidas

- El filtro es **léxico** (palabras clave), no semántico: puede dejar pasar un jailbreak parafraseado que
  evite las palabras clave, y descarta frases seguras que las contengan. Por eso hay **revisión humana**
  (`tools/prepare_pr_from_approved.py`) antes de incorporar nada a `phrases_seed.txt`.
- Ver tests en [`tests/test_filter.py`](../tests/test_filter.py).
