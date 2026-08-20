<!-- Hero -->
<p align="center">
	<img src="docs/assets/hero.svg" alt="ALUCINAJE" width="720" />
</p>

# ALUCINAJE : JAILBREAK LLM

<p align="center">
	<img src="docs/assets/ascii_art.png" alt="ASCII Art" width="720" />
</p>

<p align="center">
  <a href="https://github.com/juank3r/ALUCINAJE/actions/workflows/ci.yml"><img src="https://github.com/juank3r/ALUCINAJE/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="license" />
  <img src="https://img.shields.io/badge/python-3.9%2B-yellow.svg" alt="python" />
  <img src="https://img.shields.io/badge/enfoque-defensivo-8b5cf6.svg" alt="defensivo" />
  <img src="https://img.shields.io/badge/estado-activo-brightgreen.svg" alt="estado" />
</p>

<p align="center">
  <b>Mide la robustez de LLMs y agentes con corpus adversariales seguros.</b><br/>
  Genera variantes, evalúa frente a jailbreaks reales y produce un informe de robustez — sin redistribuir jailbreaks.
</p>

> [!IMPORTANT]
> Proyecto **defensivo**. **No** crea ni distribuye jailbreaks para evadir seguridad: su objetivo es
> **medir y reforzar la resiliencia**. De las fuentes externas se importan frases seguras y taxonomía;
> los *payloads* de jailbreak se **citan y se usan solo como set de evaluación**, nunca se copian al repo.
> Ver [`docs/JAILBREAK_RISKS.md`](docs/JAILBREAK_RISKS.md) · [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md).

---

## Índice

- [¿Por qué ALUCINAJE?](#por-qué-alucinaje)
- [Características](#características)
- [Arquitectura](#arquitectura)
- [Procedencia de los datos](#procedencia-de-los-datos)
- [Pipeline end-to-end](#pipeline-end-to-end)
- [Caso de uso: informe de robustez](#caso-de-uso-informe-de-robustez)
- [Quick start](#quick-start)
- [Estructura del repo](#estructura-del-repo)
- [Documentación](#documentación)
- [Roadmap](#roadmap)
- [FAQ](#faq)
- [Ética y contribución](#ética-y-contribución)

## ¿Por qué ALUCINAJE?

Los LLMs fallan de formas sutiles: instrucciones ambiguas, contradicciones, inyección de contexto y
jailbreaks. **Medir** esa fragilidad de forma reproducible es el primer paso para reducirla. ALUCINAJE
convierte una semilla de frases revisadas por humanos en un corpus amplio, lo prueba contra un
modelo/agente y entrega **métricas accionables** (tasa de rechazo, fugas, consistencia, latencia) — con
un enfoque responsable que **no** produce ni difunde jailbreaks.

## Características

| | Característica | Detalle |
|---|---|---|
| 🌱 | **Corpus seed-driven** | [`phrases_seed.txt`](phrases_seed.txt) curado a mano, solo contenido seguro |
| 🧬 | **Generador seguro** | [`safe_corpus_generator.py`](safe_corpus_generator.py): parafraseo + permutaciones con filtros |
| 🛡️ | **Filtro anti-jailbreak** | descarta payloads/NSFW; documentado en [`docs/FILTERING.md`](docs/FILTERING.md) |
| 🎯 | **Harness de evaluación** | [`tools/eval_jailbreaks.py`](tools/eval_jailbreaks.py) mide robustez frente a jailbreaks reales |
| 📊 | **Métricas + informe** | tasa de rechazo, fuga, latencia por categoría |
| 🔁 | **Reproducible + CI** | tests del filtro, self-test y run mock en cada PR |

## Arquitectura

![Arquitectura de ALUCINAJE](docs/assets/architecture.svg)

Detalle en [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Procedencia de los datos

Fuentes de referencia: [`verazuo/jailbreak_llms`](https://github.com/verazuo/jailbreak_llms) (dataset
CCS'24, MIT — "la web de jailbreak") y
[`Goochbeater/Spiritual-Spell-Red-Teaming`](https://github.com/Goochbeater/Spiritual-Spell-Red-Teaming)
(sin licencia → solo se cita).

![Procedencia de datos](docs/assets/data-provenance.svg)

**Hallazgo clave (verificado):** minar estos repos para sacar "frases seguras" no es viable — son casi
todo jailbreak/NSFW y el filtro léxico es débil. Por eso el seed se mantiene curado a mano:

![Embudo de saneado](docs/assets/chart-funnel.svg)

Ficha completa, licencias y atribución en [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md).

## Pipeline end-to-end

![Pipeline end-to-end](docs/assets/pipeline.svg)

Explicación paso a paso en [`docs/PIPELINE.md`](docs/PIPELINE.md).

## Caso de uso: informe de robustez

El output del proyecto es un **informe de robustez**. Los jailbreaks reales se usan como *entradas de
test* (descargados en runtime, **no** se almacenan) y se mide cuántos rechaza el modelo:

![Informe de robustez de ejemplo](docs/assets/chart-dashboard.svg)

![Tasa de rechazo por categoría](docs/assets/chart-refusal-by-category.svg)

> Gráficos con **datos de ejemplo**. Los reales los genera `tools/eval_jailbreaks.py`.
> Recorrido completo en **[`docs/EXAMPLES.md`](docs/EXAMPLES.md)**.

## Quick start

```bash
# 1) Generar variantes seguras a partir de la semilla
python safe_corpus_generator.py --seed phrases_seed.txt --out phrases_expanded.txt --factor 3 --min-len 10

# 2) Probar (modo mock, sin llamadas externas)
python tools/run_tests.py --input phrases_expanded.txt --out results --mock

# 3) Evaluar robustez frente a jailbreaks reales (requiere endpoint)
MODEL_ENDPOINT="https://tu-endpoint/infer" python tools/eval_jailbreaks.py --limit 100 --out metrics
#    …o validar la lógica sin red ni payloads:
python tools/eval_jailbreaks.py --self-test
```

## Estructura del repo

```
ALUCINAJE/
├─ phrases_seed.txt            # semilla curada (segura)
├─ safe_corpus_generator.py    # expansión segura del corpus
├─ methodology.md              # marco metodológico
├─ data/
│  └─ forbidden_question_categories.md   # taxonomía (13 categorías, solo etiquetas)
├─ tools/
│  ├─ import_and_sanitize.py   # importa + filtra fuentes externas (+ métricas)
│  ├─ run_tests.py             # runner (mock / endpoint) + métricas
│  ├─ eval_jailbreaks.py       # harness de robustez frente a jailbreaks reales
│  └─ prepare_pr_from_approved.py
├─ tests/test_filter.py        # unit tests del filtro
└─ docs/                       # arquitectura, pipeline, datos, filtrado, ejemplos, riesgos
   └─ assets/                  # diagramas y gráficos (SVG)
```

## Documentación

| Doc | Contenido |
|---|---|
| [ARCHITECTURE](docs/ARCHITECTURE.md) | Componentes y flujo de datos |
| [PIPELINE](docs/PIPELINE.md) | Etapas del pipeline |
| [DATA_SOURCES](docs/DATA_SOURCES.md) | Procedencia, licencias, estadísticas |
| [FILTERING](docs/FILTERING.md) | Cómo funciona el filtrado y sus límites |
| [EXAMPLES](docs/EXAMPLES.md) | Caso de uso completo con gráficos |
| [USAGE](docs/USAGE.md) | Uso rápido |
| [JAILBREAK_RISKS](docs/JAILBREAK_RISKS.md) | Riesgos y mitigaciones |
| [methodology](methodology.md) | Marco metodológico |

## Roadmap

- [x] Generador seguro + runner mock
- [x] Import defensivo con filtro + métricas
- [x] Diagramas de arquitectura/procedencia/pipeline
- [x] Harness de evaluación de jailbreaks (`eval_jailbreaks.py`)
- [x] CI con tests del filtro (verde)
- [ ] Clasificación automática por categoría (`forbidden_question`)
- [ ] Filtro semántico (más allá de palabras clave)
- [ ] Conector para endpoints reales (OpenAI-compatible, Anthropic)
- [ ] Publicar informes de robustez versionados

## FAQ

<details>
<summary><b>¿ALUCINAJE distribuye jailbreaks?</b></summary>

No. Los jailbreaks solo se usan como *entradas de test* (descargados en runtime, no se guardan ni se
expanden). El corpus del repo es seguro y curado a mano. Ver [`docs/FILTERING.md`](docs/FILTERING.md).
</details>

<details>
<summary><b>¿Qué es "la web de jailbreak"?</b></summary>

Es el dataset [`verazuo/jailbreak_llms`](https://github.com/verazuo/jailbreak_llms) (CCS'24): 15 140
prompts recopilados de Reddit/Discord/webs, 1 405 de ellos jailbreaks. Se usa para **evaluar**, no como semilla.
</details>

<details>
<summary><b>¿Necesito un modelo para probarlo?</b></summary>

No para el pipeline base: `--mock` funciona sin llamadas externas. Para medir robustez real necesitas un
endpoint (`MODEL_ENDPOINT`).
</details>

## Ética y contribución

- Añade frases a [`phrases_seed.txt`](phrases_seed.txt) — **solo contenido legal y seguro**.
- Abre PRs para metodología, tests o mejoras del harness (el CI valida cada PR).
- Lee la [metodología](methodology.md) y los [riesgos](docs/JAILBREAK_RISKS.md) antes de operar.

## Licencia

MIT. Al reutilizar `verazuo/jailbreak_llms` (MIT), cita el paper CCS'24 (ver [DATA_SOURCES](docs/DATA_SOURCES.md)).
