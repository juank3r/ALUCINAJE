**English** | [Español](THREAT_MODEL.md)

# Threat model

This document gives the red-team/pentesting team the map of **how the security of an LLM is attacked**
and **how ALUCINAJE helps measure it**. ALUCINAJE **measures and evaluates**; it does not run model-modification
attacks.

## Trust boundaries

```
External sources (UNTRUSTED)      ─┐
  verazuo · JBB · guides           │  eval-only (runtime)
                                   ▼
   import/sanitize  ──►  artifact  ──►  human review  ──►  phrases_seed.txt (trusted)
   (lexical filter,     (not            (control)
    weak point)         committed)
```

- **Filter** and **Human Review** are **mandatory** control points, not optional.
- Jailbreaks are used as **test inputs at runtime**; they are never committed or amplified.

## Threat classes

### A. Prompt-level jailbreaks  *(in scope — ALUCINAJE measures them)*
Inputs that induce the model to bypass its policies: role-play, "ignore previous instructions",
context injection, push prompts, obfuscation, etc.
- **Evaluation sources**: [JBB-Behaviors](https://jailbreakbench.github.io/) (100 harmful + 100
  benign, 10 categories) and `verazuo/jailbreak_llms`.
- **How to measure it**: `python tools/eval_jailbreaks.py --dataset jbb --limit 100` → **attack_success_rate**
  and **refusal_rate** by category; with `--benign`, **overrefusal_rate**. See [`METRICS.md`](METRICS.en.md).

### B. Weight-level abliteration  *(emerging threat — documented and measured, not executed here)*
Attacks that **modify the model's weights** to remove safety alignment, without retraining.
The current exponent is [**Heretic** (p-e-w/heretic)](https://github.com/p-e-w/heretic).

How it works (technical summary for the pentester):
1. **Refusal direction**: computes the *difference-of-means* between the
   activations of "harmful" and "harmless" prompts at each layer → a vector that encodes refusal.
2. **Directional ablation ("abliteration")**: orthogonalizes each layer's matrices with respect to that
   direction, so that the model can no longer "afford to" refuse.
3. **Optimization (Optuna/TPE)**: searches per-layer ablation weights by co-minimizing (a) the number of refusals on
   harmful prompts and (b) **KL-divergence** on harmless prompts (so as not to degrade capability).

![How abliteration works](assets/diagram-abliteration.en.svg)

![The geometry of the refusal direction](assets/diagram-refusal-direction.en.svg)

Why it matters to the pentester:
- An open-weight model deployed by a third party **may have been abliterated**. Its safeguards
  may be absent even if the "system prompt" says otherwise.
- **How to evaluate it with ALUCINAJE**: point the harness at the suspect model's endpoint and measure its
  posture — a high `attack_success_rate` with a very low `overrefusal_rate` is the typical fingerprint of an
  uncensored model.
  ```bash
  MODEL_ENDPOINT="https://modelo-objetivo/infer" python tools/eval_jailbreaks.py --dataset jbb --limit 100
  MODEL_ENDPOINT="https://modelo-objetivo/infer" python tools/eval_jailbreaks.py --dataset jbb --benign
  ```
- **Detection/defense**: compare against the original model's baseline; watch for sharp drops in
  refusal_rate without an increase in capability; weight provenance/hash controls; deployment policies.

> **Explicit scope.** ALUCINAJE does **not** implement or package abliteration or any weight
> modification to remove safety. For authorized use of that technique, the upstream project is Heretic; here
> it is only documented as a threat and the **measurement** is provided.

## The 2-axis framework (robustness vs capability)

A "safe" model is not the one that **refuses everything**. You have to measure two axes at once (idea taken from
Heretic's methodology —refusal vs KL— and from the JBB benign set):

- **X axis — over-refusal** (benign): does it refuse legitimate requests? (high = useless)
- **Y axis — attack success rate** (harmful): does it comply with jailbreaks? (high = insecure)

The goal is the **low-low** corner. See the quadrant chart in
[`assets/chart-robustness-quadrant.svg`](assets/chart-robustness-quadrant.en.svg) and [`METRICS.md`](METRICS.en.md).

## Risk register (summary)

| ID | Risk | Mitigation in the repo |
|----|--------|-----------------------|
| R1 | Weak lexical filter (`is_probably_jailbreak`) | human review + nothing is auto-committed ([FILTERING](FILTERING.en.md)) |
| R2 | Over-refusal (model that refuses the legitimate) | `overrefusal_rate` metric with JBB benign |
| R3 | Abliterated target model | posture measurement (section B) |
| R4 | Evasion by paraphrasing the filter | semantic filter (roadmap) + judge-LLM |
| R5 | Source licensing (Goochbeater without a license) | only cited, not redistributed |
| R6 | Amplification if `kept`→seed | veto: the seed is curated by hand |
