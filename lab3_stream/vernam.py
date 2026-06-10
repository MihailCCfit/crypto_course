"""
Шифр Вернама — посимвольный XOR текстовых файлов.
"""


def vernam_crypt(input_file, key_file, output_file):
    """XOR input_file с key_file (текстовые файлы), результат в output_file."""
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(key_file, 'r', encoding='utf-8') as fkey, \
         open(output_file, 'w', encoding='utf-8') as fout:

        while True:
            ch1 = fin.read(1)
            ch2 = fkey.read(1)

            if not ch1:
                break
            if not ch2:
                print('ПРЕДУПРЕЖДЕНИЕ: ключ короче файла, используется пробел')
                ch2 = ' '

            fout.write(chr(ord(ch1) ^ ord(ch2)))

    print(f'{input_file} XOR {key_file} -> {output_file}')
