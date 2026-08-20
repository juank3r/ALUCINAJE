
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

- **Arquitectura** — componentes y flujo de datos. See: [ARCHITECTURE](ARCHITECTURE.md)
- **Metodología** — proceso para crear, clasificar y evaluar frases. See: [methodology](../methodology.md)
- **Pipeline** — diagrama y explicación paso a paso. See: [PIPELINE](PIPELINE.md)
- **Fuentes de datos** — de dónde salen los prompts y cómo se filtran. See: [DATA_SOURCES](DATA_SOURCES.md)
- **Corpus** — semillas y cómo ampliar con `safe_corpus_generator.py`.
- **Riesgos y consecuencias** — impacto y mitigación frente a jailbreaks. See: [JAILBREAK_RISKS](JAILBREAK_RISKS.md)
- **Uso rápido** — generar corpus y ejecutar pruebas. See: [USAGE](USAGE.md)
- **Arte y galería ASCII** — obras y diagramas aportados. See: [ASCII_ART](ASCII_ART.txt)

Cómo usar esta wiki

1. Lee la **Metodología** (`methodology.md`) para comprender el marco responsable.
2. Genera el corpus con `python safe_corpus_generator.py` y revisa `phrases_expanded.txt`.
3. Ejecuta las pruebas automáticas (tbd en `docs/USAGE.md`) y analiza métricas.

Contribuye

- Añade nuevas frases en `phrases_seed.txt` (solo contenido legal y seguro).
- Abre PRs para mejoras de la metodología o nuevos tests.

