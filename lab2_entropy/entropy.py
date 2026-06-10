import math
import random
import os


def calc_frequencies(filepath):
    """Подсчёт частот символов в бинарном режиме."""
    freq = {}
    total = 0
    with open(filepath, 'rb') as f:
        while byte := f.read(1):
            freq[byte] = freq.get(byte, 0) + 1
            total += 1
    return {k: v / total for k, v in freq.items()}, total


def calc_entropy(probs):
    """Вычисление энтропии Шеннона."""
    return -sum(p * math.log2(p) for p in probs.values() if p > 0)


def generate_test_files():
    """Генерация тестовых файлов."""
    files_dir = os.path.dirname(__file__)

    # Файл из одинаковых символов
    path1 = os.path.join(files_dir, 'same_chars.bin')
    with open(path1, 'wb') as f:
        f.write(b'A' * 10000)

    # Файл из случайных 0 и 1
    path2 = os.path.join(files_dir, 'random_01.bin')
    with open(path2, 'wb') as f:
        f.write(bytes(random.choice([0, 1]) for _ in range(10000)))

    # Файл из случайных байт (0..255)
    path3 = os.path.join(files_dir, 'random_bytes.bin')
    with open(path3, 'wb') as f:
        f.write(bytes(random.randint(0, 255) for _ in range(10000)))

    # Файл со смещённым распределением (80% букв 'A', 20% случайные)
    path4 = os.path.join(files_dir, 'biased.bin')
    with open(path4, 'wb') as f:
        data = []
        for _ in range(10000):
            if random.random() < 0.8:
                data.append(ord('A'))
            else:
                data.append(random.randint(65, 90))
        f.write(bytes(data))

    return [path1, path2, path3, path4]


def main():
    print('=' * 60)
    print('ИНФОРМАЦИОННАЯ ЭНТРОПИЯ ФАЙЛА — лабораторная работа 2')
    print('=' * 60)

    while True:
        print('\n1. Вычислить энтропию своих файлов')
        print('2. Сгенерировать тестовые файлы и вычислить их энтропию')
        print('0. Выход')
        choice = input('Выберите пункт: ').strip()

        if choice == '1':
            path = input('Введите путь к файлу: ').strip()
            probs, total = calc_frequencies(path)
            entropy = calc_entropy(probs)
            print(f'\nФайл: {path}')
            print(f'Всего символов: {total}')
            print(f'Уникальных символов: {len(probs)}')
            print('\nЧастоты символов (первые 20):')
            for i, (byte, prob) in enumerate(sorted(probs.items())[:20]):
                char = chr(byte[0]) if 32 <= byte[0] < 127 else '?'
                print(f'  [{byte[0]:3d}] {char} — {prob:.6f}')
            print(f'\nЭнтропия: {entropy:.6f} бит/символ')
            print(f'Теоретический максимум: {math.log2(len(probs)):.6f} бит/символ')

        elif choice == '2':
            print('\nГенерация тестовых файлов...')
            files = generate_test_files()
            for fpath in files:
                probs, total = calc_frequencies(fpath)
                entropy = calc_entropy(probs)
                fname = os.path.basename(fpath)
                print(f'\n--- {fname} ---')
                print(f'Символов: {total}, Уникальных: {len(probs)}')
                print(f'Энтропия: {entropy:.6f} бит/символ')
                if len(probs) > 1:
                    print(f'Log2(алфавита) = {math.log2(len(probs)):.6f}')

        elif choice == '0':
            break


if __name__ == '__main__':
    main()
