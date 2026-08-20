# Fuentes de datos y procedencia

Este documento es la **fuente de verdad** sobre de dónde salen los prompts que alimentan el
pipeline de ALUCINAJE y, sobre todo, sobre **qué se importa y qué NO**.

![Procedencia de datos](assets/data-provenance.svg)

## Principio

ALUCINAJE genera **corpus adversariales seguros** para medir la robustez de LLMs. De las fuentes
externas se importan **frases adversariales seguras, taxonomía y metadatos**; los *payloads* de
jailbreak reales **se citan como fuente externa, no se copian** a este repositorio. El filtro
`is_probably_jailbreak()` de [`tools/import_and_sanitize.py`](../tools/import_and_sanitize.py)
descarta el contenido que instruye a evadir controles.

## Estado real (verificado el 2026-08-20)

- El workflow [`.github/workflows/import-and-sanitize.yml`](../.github/workflows/import-and-sanitize.yml)
  es **manual** (`workflow_dispatch`) y solo publica un **artifact** (`phrases_imported_sanitized.txt`).
- **No hay contenido importado commiteado** en el repo: `phrases_seed.txt` contiene 9 frases semilla
  escritas a mano. Import ≠ contenido en el repo.
- Para incorporar frases importadas al seed hay que pasar por **revisión humana** y
  [`tools/prepare_pr_from_approved.py`](../tools/prepare_pr_from_approved.py).

### Resultado real del import (ejecución verificada)

Al ejecutar el workflow sobre los dos repos, el saneado produjo (resumen de `.summary.json`):

| Métrica | Valor |
|---|---|
| Ficheros escaneados | 269 |
| Candidatos | 37 332 |
| Descartados (cortos) | 994 |
| Descartados (jailbreak) | 1 779 |
| Descartados (duplicados) | 7 715 |
| "kept" | 26 843 |

> [!WARNING]
> El conjunto "kept" **NO es seguro**. El filtro es **léxico** (palabras clave) y deja pasar mucho
> contenido problemático: guía operativa de jailbreak y **material sexual explícito sobre personas
> reales**. Por eso **no se vuelca al seed**: `phrases_seed.txt` se mantiene **curado a mano**. Estos
> repos son casi en su totalidad jailbreaks/NSFW, así que **no hay un corpus seguro que minar** de ellos.
> Detalle del filtrado y sus límites en [`FILTERING.md`](FILTERING.md).

## Fuentes upstream

### 1. `verazuo/jailbreak_llms`
- URL: https://github.com/verazuo/jailbreak_llms
- Descripción: dataset del paper CCS'24 — 15.140 prompts recopilados de Reddit, Discord, webs y
  datasets open-source, de los cuales **1.405 son jailbreaks**. Es "la web de jailbreak" a la que
  se refiere el proyecto.
- Popularidad: ⭐ ~3.8k.
- **Licencia: MIT** (permite reutilización con atribución).
- Estructura relevante:
  - `data/prompts/` — `jailbreak_prompts_2023_05_07.csv`, `jailbreak_prompts_2023_12_25.csv`,
    `regular_prompts_2023_05_07.csv`, `regular_prompts_2023_12_25.csv`.
  - `data/forbidden_question/` — `forbidden_question_set.csv`,
    `forbidden_question_set_with_prompts.csv.zip` (taxonomía de categorías prohibidas).
  - `code/` — utilidades del paper.
- Qué tomamos: **taxonomía de `forbidden_question` (categorías) y estadísticas**; frases neutras/
  regulares seguras tras el filtro. Los prompts de jailbreak se citan, no se importan.

### 2. `Goochbeater/Spiritual-Spell-Red-Teaming`
- URL: https://github.com/Goochbeater/Spiritual-Spell-Red-Teaming
- Descripción: colección de guías de red-teaming/jailbreak por proveedor (principalmente Claude).
- Popularidad: ⭐ ~3.2k.
- **Licencia: ninguna declarada** → por defecto *todos los derechos reservados*. **No se debe
  redistribuir su contenido**; solo se cita/enlaza.
- Estructura (`Jailbreak-Guide/`): `Anthropic/` (Claude 3.7/4, Opus 4.5/4.6, Claude Code, Fable 5…),
  `ChatGPT/`, `Gemini/`, `Grok/`, `Other LLMs/`, `System Prompts/`, `ENI-Tutor/`,
  `Jailbroken POE bots/`.
- Qué tomamos: **solo la taxonomía/estructura como referencia** (qué categorías de ataque existen).
  Ningún payload se copia por licencia y por política del proyecto.

## Cómo se importa (flujo defensivo)

1. Ejecutar el workflow **Import and Sanitize External Prompts** (dispatch) o localmente:
   ```bash
   python tools/import_and_sanitize.py \
     --repos https://github.com/verazuo/jailbreak_llms \
             https://github.com/Goochbeater/Spiritual-Spell-Red-Teaming \
     --out phrases_imported_sanitized.txt
   ```
   Genera además `phrases_imported_sanitized.summary.json` con el **resumen de metadatos**
   (nº de repos, ficheros escaneados, candidatos, descartados por el filtro, frases finales).
2. **Revisar** `phrases_imported_sanitized.txt` a mano (ver aviso arriba: el filtro es débil).
3. Aprobar y proponer PR con
   `python tools/prepare_pr_from_approved.py --approved approved_phrases.txt`.

## Taxonomía importada

Lo que sí se importa de forma segura es la **taxonomía de categorías** de `forbidden_question`
(solo etiquetas, no payloads): ver [`data/forbidden_question_categories.md`](../data/forbidden_question_categories.md).

## Uso correcto de los jailbreaks: evaluación (no semilla)

Los prompts de jailbreak **no se copian ni se expanden**. La forma correcta de usarlos es como
**conjunto de evaluación**: [`tools/eval_jailbreaks.py`](../tools/eval_jailbreaks.py) los descarga en
tiempo de test desde el upstream (MIT), los envía a un endpoint y calcula la **tasa de rechazo**, sin
guardarlos en el repo.

```bash
# self-test (sin red ni payloads)
python tools/eval_jailbreaks.py --self-test
# contra un endpoint real
MODEL_ENDPOINT="https://tu-endpoint/infer" python tools/eval_jailbreaks.py --limit 100 --out metrics
```

## Atribución

Al reutilizar `verazuo/jailbreak_llms` (MIT), citar:
> H. Shen et al., "In-The-Wild Jailbreak Prompts on LLMs", ACM CCS 2024. Repo: verazuo/jailbreak_llms.

`Goochbeater/Spiritual-Spell-Red-Teaming` se enlaza como referencia; su contenido no se redistribuye.
