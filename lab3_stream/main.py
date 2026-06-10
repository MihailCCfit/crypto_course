"""
Лабораторная работа 3 — Шифр Вернама и поточные шифры.
"""
import os
from lcg import generate_key_file
from vernam import vernam_crypt
from rc4 import rc4_crypt_file


def main():
    base_dir = os.path.dirname(__file__)

    while True:
        print('\n' + '=' * 60)
        print('ПОТОЧНЫЕ ШИФРЫ — лабораторная работа 3')
        print('=' * 60)
        print('1. Сгенерировать ключевой файл (LCG)')
        print('2. Зашифровать/расшифровать шифром Вернама (XOR)')
        print('3. Зашифровать/расшифровать поточным шифром RC4')
        print('0. Выход')
        choice = input('Выберите пункт: ').strip()

        if choice == '1':
            path = input('Путь для сохранения ключа (по умолчанию key.txt): ').strip()
            if not path:
                path = os.path.join(base_dir, 'key.txt')
            size = int(input('Длина ключа в символах: '))
            seed_str = input('Seed (пусто = авто): ').strip()
            seed = int(seed_str) if seed_str else None
            generate_key_file(path, size, seed)

        elif choice == '2':
            inp = input('Файл для шифрования/расшифровки: ').strip()
            key = input('Файл с ключом: ').strip()
            out = input('Выходной файл: ').strip()
            vernam_crypt(inp, key, out)

        elif choice == '3':
            inp = input('Файл для шифрования/расшифровки: ').strip()
            key_str = input('Ключ (строка): ').strip()
            out = input('Выходной файл: ').strip()
            rc4_crypt_file(inp, key_str, out)

        elif choice == '0':
            break


if __name__ == '__main__':
    main()
