import random
import pathlib
from itertools import permutations

BASE = pathlib.Path(__file__).parent

def load_seed(path: pathlib.Path):
    return [line.strip() for line in path.read_text(encoding='utf8').splitlines() if line.strip() and not line.startswith('#')]

def simple_paraphrases(phrase: str):
    # Regla simple de variación segura: sinónimos y reordenado de cláusulas simples
    swaps = [phrase]
    tokens = phrase.split()
    if len(tokens) > 4:
        swaps.append(' '.join(tokens[::-1]))
    # pequeñas sustituciones seguras
    subs = {
        'explica': 'describe',
        'cómo': 'de qué manera',
        'pasos': 'procedimiento',
        'auditar': 'evaluar',
    }
    for k, v in subs.items():
        if k in phrase:
            swaps.append(phrase.replace(k, v))
    return list(dict.fromkeys(swaps))

def diversify(seed_path: pathlib.Path, out_path: pathlib.Path, factor: int = 5):
    seed = load_seed(seed_path)
    out = []
    for p in seed:
        out.append(p)
        paras = simple_paraphrases(p)
        out.extend(paras)
        # combinaciones cortas para crear variaciones
        words = p.split()
        if len(words) <= 6:
            for perm in permutations(words, min(3, len(words))):
                out.append(' '.join(perm))
        # mezclas aleatorias controladas
        for _ in range(factor):
            w = words[:]
            random.shuffle(w)
            out.append(' '.join(w))
    # deduplicar y escribir
    unique = []
    for s in out:
        s2 = ' '.join(s.split())
        if s2 not in unique:
            unique.append(s2)
    out_path.write_text('\n'.join(unique), encoding='utf8')
    print(f'Generadas {len(unique)} frases en {out_path}')

if __name__ == '__main__':
    seed = BASE / 'phrases_seed.txt'
    out = BASE / 'phrases_expanded.txt'
    diversify(seed, out, factor=3)
