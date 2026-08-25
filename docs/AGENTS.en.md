**English** | [Español](AGENTS.md)

# Agent attack surface

AI agents (with tools, memory, and actions) extend the attack surface beyond an LLM chat.
`tools/agent_probes.py` runs a battery mapped to **OWASP Top 10 for Agentic Applications** + LLM
Top 10 + MITRE ATLAS, **always with benign canaries** (marker, fake secret, fake sink).

## Included probes

| Probe | OWASP | Severity | What it detects |
|---|---|---|---|
| `direct_injection` | A1 Agent Goal Hijack | medium | The agent obeys a directly injected instruction |
| `indirect_injection` | A1 (indirect) | high | Instruction hidden in retrieved content (doc/tool output) |
| `system_prompt_leak` | LLM07 System Prompt Leakage | high | Reveals its system prompt / configuration |
| `secret_exfiltration` | LLM06 Sensitive Info Disclosure | critical | Routes a canary-secret to a fake sink (exfil channel) |
| `tool_misuse` | A2 Tool Misuse | high | Calls an unauthorized tool via injection |
| `excessive_agency` | A3 Excessive Agency | high | Executes a destructive action outside its read-only role |

## How it works (safe by design)

- Each probe inserts a **benign marker**; success is detected if OUR canary appears where it
  shouldn't (e.g. the model emits the injected token, reveals the canary-secret, or "sends" the secret to the
  fake sink `http://sink.<canary>.invalid`). There is **never** real exfiltration, deletion, or actions with impact.
- The target must be authorized in `scope.yaml` (the gate rejects everything else).
- The report stores only the result of the technique and which canary matched; it does **not** store the raw
  output of the target (PII/secrets red line).

## Usage (authorized)

```bash
MODEL_ENDPOINT="http://127.0.0.1:11434" \
  python tools/agent_probes.py --scope scope.yaml --service ollama --model llama3 --out metrics

python tools/agent_probes.py --self-test   # offline, valida la lógica de detección
```

## Copilot class (M365 / Copilot Studio / GitHub)

The same techniques apply to Copilot-style assistants (indirect injection via document/email,
ASCII-smuggling, exfil marker). References: Zenity ("Living off Microsoft Copilot" / LOLCopilot),
EchoLeak (zero-click), Embrace The Red. **Only against your own authorized tenant**, with canaries.

See [`THREAT_MODEL.md`](THREAT_MODEL.en.md) and [`RED_TEAM.md`](RED_TEAM.en.md).
