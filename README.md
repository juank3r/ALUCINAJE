
<!-- Hero -->
<p align="center">
	<img src="docs/assets/hero.png" alt="ALUCINAJE" width="720" />
</p>

# ALUCINAJE — Robustez y pruebas adversariales responsables

<p align="center">
	<img src="docs/assets/ascii_art.png" alt="ASCII Art" width="720" />
</p>

![license](https://img.shields.io/badge/license-MIT-blue.svg)
![issues](https://img.shields.io/badge/issues-welcome-brightgreen.svg)
![python](https://img.shields.io/badge/python-3.8%2B-yellow.svg)

Proyecto para generar corpus seguros, diseñar metodologías de prueba y evaluar la robustez de modelos de lenguaje y agentes.

Highlights

- Seed-driven corpus: `phrases_seed.txt` contiene frases semilla revisadas.
- Generador seguro: `safe_corpus_generator.py` expande la semilla mediante parafraseo y permutaciones controladas.
- Wiki y documentación: carpeta `docs/` con arquitectura, pipeline y riesgos.

Important: Este repositorio evita crear o distribuir "jailbreaks" destinados a evadir sistemas de seguridad. Nuestro objetivo es mejorar la resiliencia y cumplimiento.

## Contenido rápido

- [Wiki / Home](docs/HOME.md)
- [Arquitectura](docs/ARCHITECTURE.md)
- [Pipeline](docs/PIPELINE.md)
- [Riesgos de jailbreak](docs/JAILBREAK_RISKS.md)
- [Generador seguro](safe_corpus_generator.py)
- [Seed de frases](phrases_seed.txt)

## Arte ASCII (imagen)

He renderizado el arte ASCII como una imagen y la he incluido abajo para que se vea bien en GitHub:

<p align="center">
	<img src="docs/assets/ascii_art.svg" alt="ASCII Art" width="800" />
</p>

Si prefieres una versión PNG lista para descargar, dime y la genero (requiere Python en local para rasterizar o puedo subir una versión si lo autoriza).
## Quick start

```bash
python safe_corpus_generator.py
# revisa `phrases_expanded.txt`
```

## Contribuir

- Añade nuevas frases a `phrases_seed.txt` (sólo contenido seguro).
- Abre PRs para mejoras de la metodología o nuevos tests.

