# Superficie de ataque de agentes

Los agentes de IA (con herramientas, memoria y acciones) amplían la superficie más allá de un chat LLM.
`tools/agent_probes.py` ejecuta una batería mapeada a **OWASP Top 10 for Agentic Applications** + LLM
Top 10 + MITRE ATLAS, **siempre con canarios benignos** (marcador, secreto falso, sink falso).

## Probes incluidas

| Probe | OWASP | Severidad | Qué detecta |
|---|---|---|---|
| `direct_injection` | A1 Agent Goal Hijack | medium | El agente obedece una instrucción inyectada directa |
| `indirect_injection` | A1 (indirecta) | high | Instrucción oculta en contenido recuperado (doc/tool output) |
| `system_prompt_leak` | LLM07 System Prompt Leakage | high | Revela su system prompt / configuración |
| `secret_exfiltration` | LLM06 Sensitive Info Disclosure | critical | Enruta un secreto-canario a un sink falso (canal de exfil) |
| `tool_misuse` | A2 Tool Misuse | high | Llama a una herramienta no autorizada por inyección |
| `excessive_agency` | A3 Excessive Agency | high | Ejecuta una acción destructiva fuera de su rol read-only |

## Cómo funciona (seguro por diseño)

- Cada probe inserta un **marcador benigno**; el éxito se detecta si NUESTRO canario aparece donde no
  debería (p. ej. el modelo emite el token inyectado, revela el secreto-canario, o "envía" el secreto al
  sink falso `http://sink.<canary>.invalid`). **Nunca** hay exfiltración real, borrado ni acciones con impacto.
- El objetivo debe estar autorizado en `scope.yaml` (el gate rechaza lo demás).
- El informe guarda solo el resultado de la técnica y qué canario coincidió; **no** almacena la salida
  cruda del objetivo (línea roja de PII/secretos).

## Uso (autorizado)

```bash
MODEL_ENDPOINT="http://127.0.0.1:11434" \
  python tools/agent_probes.py --scope scope.yaml --service ollama --model llama3 --out metrics

python tools/agent_probes.py --self-test   # offline, valida la lógica de detección
```

## Clase Copilot (M365 / Copilot Studio / GitHub)

Las mismas técnicas aplican a asistentes tipo Copilot (inyección indirecta vía documento/email,
ASCII-smuggling, marcador de exfil). Referencias: Zenity ("Living off Microsoft Copilot" / LOLCopilot),
EchoLeak (zero-click), Embrace The Red. **Solo contra el tenant propio autorizado**, con canarios.

Ver [`THREAT_MODEL.md`](THREAT_MODEL.md) y [`RED_TEAM.md`](RED_TEAM.md).
