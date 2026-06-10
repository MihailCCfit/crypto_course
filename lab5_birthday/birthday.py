"""
Демонстрация парадокса дней рождения на криптографической хеш-функции.

Используем усечённый SHA-256 (N бит) и ищем коллизию 2-го рода.
Парадокс: для 50% вероятности коллизии нужно около 1.25 * sqrt(2^N) попыток.
"""

import hashlib
import random
import string
import math


def truncated_hash(data, bits):
    """SHA-256, усечённый до заданного числа бит."""
    h = hashlib.sha256(data).digest()
    byte_len = (bits + 7) // 8
    val = int.from_bytes(h[:byte_len], 'big')
    mask = (1 << bits) - 1
    return val & mask


def random_message(length=8):
    """Генерирует случайную строку."""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length)).encode()


def find_collision(bits):
    """Ищет коллизию 2-го рода для усечённого хеша."""
    seen = {}
    attempts = 0
    expected = int(1.25 * math.sqrt(2 ** bits))

    while True:
        msg = random_message()
        h = truncated_hash(msg, bits)
        attempts += 1

        if h in seen and seen[h] != msg:
            return seen[h], msg, h, attempts, expected

        seen[h] = msg


def main():
    print('=' * 65)
    print('ПАРАДОКС ДНЕЙ РОЖДЕНИЯ НА ХЕШ-ФУНКЦИИ — лабораторная 5')
    print('=' * 65)
    print()

    while True:
        print('1. Поиск коллизии для усечённого SHA-256 (заданное число бит)')
        print('2. Демо для нескольких размеров хеша (8, 12, 16, 20 бит)')
        print('0. Выход')
        choice = input('Выберите пункт: ').strip()

        if choice == '1':
            bits = int(input('Размер хеша в битах (например, 16): '))
            print(f'\nПоиск коллизии для хеша {bits} бит...')
            print(f'Ожидаемое число попыток (50%): ~{int(1.25 * math.sqrt(2 ** bits))}')
            msg1, msg2, hash_val, attempts, expected = find_collision(bits)
            print(f'\nКоллизия найдена!')
            print(f'Сообщение 1: {msg1.decode()}')
            print(f'Сообщение 2: {msg2.decode()}')
            print(f'Хеш ({bits} бит): {hash_val:0{bits // 4}x}')
            print(f'Потребовалось попыток: {attempts}')
            print(f'Ожидалось (~50%): {expected}')
            print(f'Отношение: {attempts / expected:.2f}')

        elif choice == '2':
            for bits in [8, 12, 16, 20]:
                print(f'\n--- {bits} бит ---')
                total = 2 ** bits
                expected = int(1.25 * math.sqrt(total))
                print(f'Пространство значений: {total}')
                print(f'Ожидаемое число попыток (50%): {expected}')

                msg1, msg2, hash_val, attempts, _ = find_collision(bits)
                print(f'Найдено за {attempts} попыток')
                print(f'Отношение: {attempts / expected:.2f}')
                print(f'  Msg1: {msg1.decode()}')
                print(f'  Msg2: {msg2.decode()}')
                print(f'  Hash: {hash_val:0{(bits + 3) // 4}x}')

        elif choice == '0':
            break


if __name__ == '__main__':
    main()
