
## ALUCINAJE — Wiki

Bienvenido a ALUCINAJE — un proyecto para generar, testar y mejorar la robustez de LLMs y agentes mediante corpus adversariales responsables.

================================================================================

						  .----.   .----.  .----.   .----.
						 /      \ /      \/      \ /      \
						/  .-.  /  .-.  /  .-.  /  .-.  /
					   |  (   )|  (   )|  (   )|  (   )|
						\  `-'  \  `-'  \  `-'  \  `-'  /
						 `-----' `-----' `-----' `-----'

================================================================================

Secciones principales (salta a cualquiera):

- **Introducción y ética** — visión y reglas de uso responsable. See: [ARCHITECTURE](ARCHITECTURE.md)
- **Metodología** — proceso para crear, clasificar y evaluar frases.
- **Pipeline** — diagrama ASCII y explicación paso a paso. See: [PIPELINE](PIPELINE.md)
- **Corpus** — semillas y cómo ampliar con `safe_corpus_generator.py`.
- **Riesgos y consecuencias** — impacto y mitigación frente a jailbreaks. See: [JAILBREAK_RISKS](JAILBREAK_RISKS.md)
- **Arte y galería ASCII** — incluye obras y diagramas aportados. See: [ASCII_ART](ASCII_ART.txt)

Cómo usar esta wiki

1. Lee la **Metodología** (`methodology.md`) para comprender el marco responsable.
2. Genera el corpus con `python safe_corpus_generator.py` y revisa `phrases_expanded.txt`.
3. Ejecuta las pruebas automáticas (tbd en `docs/USAGE.md`) y analiza métricas.

Contribuye

- Añade nuevas frases en `phrases_seed.txt` (solo contenido legal y seguro).
- Abre PRs para mejoras de la metodología o nuevos tests.

