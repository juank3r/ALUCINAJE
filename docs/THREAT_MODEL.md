# Modelo de amenaza

Este documento da al equipo de red-team/pentesting el mapa de **cómo se ataca la seguridad de un LLM**
y **cómo ALUCINAJE ayuda a medirlo**. ALUCINAJE **mide y evalúa**; no ejecuta ataques de modificación
de modelos.

## Fronteras de confianza

```
Fuentes externas (NO confiables)  ─┐
  verazuo · JBB · guías            │  eval-only (runtime)
                                   ▼
   import/sanitize  ──►  artifact  ──►  revisión humana  ──►  phrases_seed.txt (confiable)
   (filtro léxico,        (no se           (control)
    punto débil)          commitea)
```

- **Filter** y **Human Review** son puntos de control **obligatorios**, no opcionales.
- Los jailbreaks se usan como **entradas de test en runtime**; nunca se commitean ni se amplifican.

## Clases de amenaza

### A. Jailbreaks a nivel de prompt  *(en alcance — ALUCINAJE los mide)*
Entradas que inducen al modelo a saltarse políticas: role-play, "ignore previous instructions",
inyección de contexto, push prompts, ofuscación, etc.
- **Fuentes de evaluación**: [JBB-Behaviors](https://jailbreakbench.github.io/) (100 dañinos + 100
  benignos, 10 categorías) y `verazuo/jailbreak_llms`.
- **Cómo medirlo**: `python tools/eval_jailbreaks.py --dataset jbb --limit 100` → **attack_success_rate**
  y **refusal_rate** por categoría; con `--benign`, **overrefusal_rate**. Ver [`METRICS.md`](METRICS.md).

### B. Abliteration a nivel de pesos  *(amenaza emergente — se documenta y se mide, no se ejecuta aquí)*
Ataques que **modifican los pesos** del modelo para eliminar la alineación de seguridad, sin reentrenar.
El exponente actual es [**Heretic** (p-e-w/heretic)](https://github.com/p-e-w/heretic).

Cómo funciona (resumen técnico para el pentester):
1. **Dirección de rechazo**: calcula la diferencia de medias (*difference-of-means*) entre las
   activaciones de prompts "dañinos" y "inofensivos" en cada capa → un vector que codifica el rechazo.
2. **Ablación direccional ("abliteration")**: ortogonaliza las matrices de cada capa respecto a esa
   dirección, de modo que el modelo deja de "poder" rechazar.
3. **Optimización (Optuna/TPE)**: busca pesos de ablación por capa co-minimizando (a) nº de rechazos en
   prompts dañinos y (b) **KL-divergencia** en prompts inofensivos (para no degradar la capacidad).

Por qué importa al pentester:
- Un modelo open-weight desplegado por un tercero **puede haber sido abliterado**. Sus salvaguardas
  pueden estar ausentes aunque el "system prompt" diga lo contrario.
- **Cómo evaluarlo con ALUCINAJE**: apunta el harness al endpoint del modelo sospechoso y mide su
  postura — un `attack_success_rate` alto con `overrefusal_rate` muy bajo es la huella típica de un
  modelo descensurado.
  ```bash
  MODEL_ENDPOINT="https://modelo-objetivo/infer" python tools/eval_jailbreaks.py --dataset jbb --limit 100
  MODEL_ENDPOINT="https://modelo-objetivo/infer" python tools/eval_jailbreaks.py --dataset jbb --benign
  ```
- **Detección/defensa**: comparar contra la línea base del modelo original; vigilar caídas bruscas de
  refusal_rate sin subida de capacidad; controles de procedencia/hash de pesos; políticas de despliegue.

> **Alcance explícito.** ALUCINAJE **no** implementa ni empaqueta abliteration ni ninguna modificación de
> pesos para quitar seguridad. Para uso autorizado de esa técnica, el proyecto upstream es Heretic; aquí
> solo se documenta como amenaza y se ofrece la **medición**.

## El marco de 2 ejes (robustez vs capacidad)

Un modelo "seguro" no es el que **rechaza todo**. Hay que medir dos ejes a la vez (idea tomada de la
metodología de Heretic —rechazo vs KL— y de los benignos de JBB):

- **Eje X — over-refusal** (benignos): ¿rechaza peticiones legítimas? (alto = inútil)
- **Eje Y — attack success rate** (dañinos): ¿cumple jailbreaks? (alto = inseguro)

El objetivo es la esquina **bajo-bajo**. Ver el gráfico de cuadrante en
[`assets/chart-robustness-quadrant.svg`](assets/chart-robustness-quadrant.svg) y [`METRICS.md`](METRICS.md).

## Registro de riesgos (resumen)

| ID | Riesgo | Mitigación en el repo |
|----|--------|-----------------------|
| R1 | Filtro léxico débil (`is_probably_jailbreak`) | revisión humana + nada se auto-commitea ([FILTERING](FILTERING.md)) |
| R2 | Over-refusal (modelo que rechaza lo legítimo) | métrica `overrefusal_rate` con benignos JBB |
| R3 | Modelo objetivo abliterado | medición de postura (sección B) |
| R4 | Evasión por parafraseo del filtro | filtro semántico (roadmap) + judge-LLM |
| R5 | Licencia de fuentes (Goochbeater sin licencia) | solo se cita, no se redistribuye |
| R6 | Amplificación si `kept`→seed | veto: el seed se cura a mano |
