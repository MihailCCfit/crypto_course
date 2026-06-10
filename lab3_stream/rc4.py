"""
Поточный шифр RC4 (Rivest Cipher 4) для текстовых файлов.
"""


def rc4_keystream(key_bytes):
    """Генератор ключевого потока RC4."""
    key_len = len(key_bytes)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key_bytes[i % key_len]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) % 256]


def rc4_crypt_file(input_file, key_str, output_file):
    """Шифрует/расшифровывает текстовый файл с помощью RC4."""
    key_bytes = key_str.encode('utf-8')
    ks = rc4_keystream(key_bytes)

    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:

        while ch := fin.read(1):
            fout.write(chr(ord(ch) ^ next(ks)))

    print(f'RC4: {input_file} -> {output_file}')
