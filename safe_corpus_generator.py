import argparse
import random
import pathlib
import re
from itertools import permutations
from typing import List

BASE = pathlib.Path(__file__).parent


def load_seed(path: pathlib.Path) -> List[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def simple_paraphrases(phrase: str) -> List[str]:
    # Variaciones seguras y controladas (no generan instrucciones para evadir sistemas)
    swaps = [phrase]
    tokens = phrase.split()
    if len(tokens) > 3:
        swaps.append(" ".join(tokens[::-1]))

    subs = {
        "explica": "describe",
        "cómo": "de qué manera",
        "pasos": "procedimiento",
        "auditar": "evaluar",
    }
    for k, v in subs.items():
        if k in phrase:
            swaps.append(phrase.replace(k, v))

    # Añadir formas cortas con prefijos de cortesía que mantienen el contexto
    swaps.append("Por favor, " + phrase)
    swaps.append("En resumen: " + phrase)
    # Normalizar duplicados y devolver
    return list(dict.fromkeys(s for s in swaps if s))


def is_safe(phrase: str, banned_keywords: List[str]) -> bool:
    low = phrase.lower()
    for k in banned_keywords:
        if k in low:
            return False
    # filtro simple de caracteres: permitir letras, dígitos y puntuación básica
    if not re.match(r"^[\w\s\p{P}\,\.;:\-¡!¿?()\[\]<>%&]+$", phrase, flags=re.UNICODE):
        # si la regex falla, rechazamos la frase
        return False
    return True


def diversify(
    seed_path: pathlib.Path,
    out_path: pathlib.Path,
    factor: int = 5,
    min_len: int = 5,
    max_len: int = 200,
    max_total: int = 5000,
    banned_keywords: List[str] = None,
):
    if banned_keywords is None:
        banned_keywords = [
            "bypass",
            "evadir",
            "evade",
            "jailbreak",
            "desactivar",
            "disable",
            "overrid",
            "saltarse",
        ]

    seed = load_seed(seed_path)
    out = []
    for p in seed:
        out.append(p)
        paras = simple_paraphrases(p)
        out.extend(paras)

        words = p.split()
        # permutaciones cortas controladas
        if 2 <= len(words) <= 6:
            for perm in permutations(words, min(3, len(words))):
                out.append(" ".join(perm))

        # mezclas aleatorias controladas
        for _ in range(factor):
            w = words[:]
            random.shuffle(w)
            out.append(" ".join(w))

    # normalizar espacios, deduplicar y aplicar filtros
    unique = []
    for s in out:
        s2 = " ".join(s.split())
        if s2 in unique:
            continue
        if len(s2) < min_len or len(s2) > max_len:
            continue
        if not is_safe(s2, banned_keywords):
            continue
        unique.append(s2)
        if len(unique) >= max_total:
            break

    out_path.write_text("\n".join(unique), encoding="utf8")
    print(f"Generadas {len(unique)} frases en {out_path}")
    return unique


def cli():
    p = argparse.ArgumentParser(description="Generador seguro y diversificador de frases (seed-driven)")
    p.add_argument("--seed", default=BASE / "phrases_seed.txt", help="Ruta al fichero seed")
    p.add_argument("--out", default=BASE / "phrases_expanded.txt", help="Fichero de salida")
    p.add_argument("--factor", type=int, default=3, help="Variaciones aleatorias por frase")
    p.add_argument("--min-len", type=int, default=10, help="Longitud mínima de frase (caracteres)")
    p.add_argument("--max-len", type=int, default=200, help="Longitud máxima de frase (caracteres)")
    p.add_argument("--max-total", type=int, default=5000, help="Máximo total de frases generadas")
    args = p.parse_args()

    seed = pathlib.Path(args.seed)
    out = pathlib.Path(args.out)
    diversify(seed, out, factor=args.factor, min_len=args.min_len, max_len=args.max_len, max_total=args.max_total)


if __name__ == "__main__":
    cli()
