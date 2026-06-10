"""
Линейный конгруэнтный генератор (LCG).
Формула: X_{n+1} = (a * X_n + c) mod m

Генерирует текстовый ключевой файл из печатных символов.
"""

import string

CHARSET = string.ascii_letters + string.digits


def lcg(seed, a=1664525, c=1013904223, m=2**32):
    """Генератор псевдослучайных чисел LCG."""
    x = seed
    while True:
        x = (a * x + c) % m
        yield x


def generate_key_file(filepath, size, seed=None):
    """Генерирует текстовый файл-ключ заданной длины (символов)."""
    if seed is None:
        import time
        seed = int(time.time())

    gen = lcg(seed)
    with open(filepath, 'w', encoding='utf-8') as f:
        for _ in range(size):
            f.write(CHARSET[next(gen) % len(CHARSET)])

    print(f'Сгенерирован ключевой файл {filepath} ({size} символов, seed={seed})')
