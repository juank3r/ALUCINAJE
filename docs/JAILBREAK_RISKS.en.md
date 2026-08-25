**English** | [Español](JAILBREAK_RISKS.md)

# Consequences and risks of "jailbreaks"

What is a "jailbreak" (summary)
- In this context, a "jailbreak" refers to techniques that attempt to induce a model to ignore policies, reveal sensitive information, or perform unauthorized actions.
- In addition to **prompt-level** jailbreaks, there is an emerging **weight-level** threat: the
  *abliteration* (directional ablation) removes safety alignment by modifying the model. See
  [`THREAT_MODEL.en.md`](THREAT_MODEL.en.md) for the details and how to measure an abliterated model.

Legal and compliance risks
- Disclosure of personal data or trade secrets can expose the company to fines, regulatory sanctions (GDPR, etc.), and legal claims.

Reputational risks
- Publishing or allowing models to respond with harmful information can erode the trust of customers and partners.

Security and operational risks
- Leakage of credentials or attack paths.
- Automation of malicious activity if the model responds with operational instructions.

Ethical risks
- Misuse by third parties: weapons, fraud, disinformation.

Recommended mitigations
- Do not include real jailbreaks in public corpora.
- Filter and anonymize test data.
- Maintain access controls, auditing, and human review for borderline cases.
- Response plan: lockdown, credential rotation, notification to stakeholders.

Note for testers
- The goal of our tests is to measure resilience and strengthen controls, not to produce lists of jailbreaks that circulate publicly.
