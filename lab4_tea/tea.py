"""
Блочный шифр TEA (Tiny Encryption Algorithm).
Размер блока: 8 байт, размер ключа: 16 байт.
"""

import struct

DELTA = 0x9E3779B9
ROUNDS = 32
MASK32 = 0xFFFFFFFF


def _pad(data, block_size=8):
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def _unpad(data):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 8:
        raise ValueError('Некорректный padding')
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError('Некорректный padding')
    return data[:-pad_len]


def tea_encrypt_block(block, key):
    v0, v1 = struct.unpack('!2I', block)
    k0, k1, k2, k3 = struct.unpack('!4I', key)
    s = 0
    for _ in range(ROUNDS):
        s = (s + DELTA) & MASK32
        v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1))) & MASK32
        v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3))) & MASK32
    return struct.pack('!2I', v0, v1)


def tea_decrypt_block(block, key):
    v0, v1 = struct.unpack('!2I', block)
    k0, k1, k2, k3 = struct.unpack('!4I', key)
    s = (DELTA * ROUNDS) & MASK32
    for _ in range(ROUNDS):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3))) & MASK32
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1))) & MASK32
        s = (s - DELTA) & MASK32
    return struct.pack('!2I', v0, v1)


def tea_encrypt_file(input_path, output_path, key):
    """Зашифрование файла блочным шифром TEA."""
    key_bytes = key if isinstance(key, bytes) else key.encode('utf-8')
    key_bytes = key_bytes[:16].ljust(16, b'\x00')

    with open(input_path, 'rb') as fin:
        data = fin.read()
    padded = _pad(data)

    with open(output_path, 'wb') as fout:
        for i in range(0, len(padded), 8):
            block = padded[i:i + 8]
            fout.write(tea_encrypt_block(block, key_bytes))

    print(f'TEA encrypt: {input_path} -> {output_path}')


def tea_decrypt_file(input_path, output_path, key):
    """Расшифрование файла блочным шифром TEA."""
    key_bytes = key if isinstance(key, bytes) else key.encode('utf-8')
    key_bytes = key_bytes[:16].ljust(16, b'\x00')

    with open(input_path, 'rb') as fin:
        data = fin.read()

    decrypted = b''
    for i in range(0, len(data), 8):
        decrypted += tea_decrypt_block(data[i:i + 8], key_bytes)

    unpadded = _unpad(decrypted)
    with open(output_path, 'wb') as fout:
        fout.write(unpadded)

    print(f'TEA decrypt: {input_path} -> {output_path}')


def main():
    import os

    while True:
        print('\n' + '=' * 60)
        print('БЛОЧНЫЙ ШИФР TEA — лабораторная работа 4')
        print('=' * 60)
        print('1. Зашифровать файл (TEA)')
        print('2. Расшифровать файл (TEA)')
        print('3. Демо: создать тестовый файл, зашифровать и расшифровать')
        print('0. Выход')
        choice = input('Выберите пункт: ').strip()

        if choice == '1':
            inp = input('Входной файл: ').strip()
            out = input('Выходной файл: ').strip()
            key = input('Ключ (строка, до 16 символов): ').strip()
            tea_encrypt_file(inp, out, key)

        elif choice == '2':
            inp = input('Входной файл: ').strip()
            out = input('Выходной файл: ').strip()
            key = input('Ключ (строка, до 16 символов): ').strip()
            tea_decrypt_file(inp, out, key)

        elif choice == '3':
            base = os.path.dirname(__file__)
            test_file = os.path.join(base, 'test_input.txt')
            enc_file = os.path.join(base, 'test_encrypted.bin')
            dec_file = os.path.join(base, 'test_decrypted.txt')
            key = 'super_secret_key'

            # Создаём тестовый файл
            with open(test_file, 'wb') as f:
                f.write(b'Hello, TEA cipher! This is a test file for Lab 4.' * 10)

            print(f'\nСоздан тестовый файл: {test_file}')
            tea_encrypt_file(test_file, enc_file, key)
            tea_decrypt_file(enc_file, dec_file, key)

            with open(test_file, 'rb') as f:
                orig = f.read()
            with open(dec_file, 'rb') as f:
                decr = f.read()

            print(f'\nИсходный размер: {len(orig)} байт')
            print(f'Расшифрованный размер: {len(decr)} байт')
            print(f'Совпадают: {orig == decr}')
            print(f'Первые 100 байт исходного: {orig[:100]}')
            print(f'Первые 100 байт расшифрованного: {decr[:100]}')

        elif choice == '0':
            break


if __name__ == '__main__':
    main()
