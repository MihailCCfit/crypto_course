import os
import urllib.request

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET_LEN = 26


def caesar_encrypt(text, key):
    result = []
    for ch in text:
        if ch.isalpha():
            base = 'a' if ch.islower() else 'A'
            result.append(chr((ord(ch) - ord(base) + key) % ALPHABET_LEN + ord(base)))
        else:
            result.append(ch)
    return ''.join(result)


def caesar_decrypt(text, key):
    return caesar_encrypt(text, (ALPHABET_LEN - key) % ALPHABET_LEN)


def known_plaintext_attack(plaintext, ciphertext):
    for p, c in zip(plaintext, ciphertext):
        if p.isalpha() and c.isalpha():
            p_base = ord('a') if p.islower() else ord('A')
            c_base = ord('a') if c.islower() else ord('A')
            return (ord(c) - c_base - (ord(p) - p_base)) % ALPHABET_LEN
    return None


def brute_force(ciphertext):
    results = []
    for key in range(ALPHABET_LEN):
        results.append((key, caesar_decrypt(ciphertext, key)))
    return results


def download_dictionary():
    url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words.txt'
    dict_path = os.path.join(os.path.dirname(__file__), 'words.txt')
    if not os.path.exists(dict_path):
        print('Загрузка словаря...')
        urllib.request.urlretrieve(url, dict_path)
    with open(dict_path, 'r', encoding='utf-8') as f:
        return set(word.strip().lower() for word in f.readlines())


def dictionary_attack(ciphertext):
    dictionary = download_dictionary()
    best_key = None
    best_decrypted = None
    best_ratio = 0

    for key in range(ALPHABET_LEN):
        decrypted = caesar_decrypt(ciphertext, key)
        words = decrypted.lower().split()
        if len(words) == 0:
            continue
        meaningful = sum(1 for w in words if w.strip('.,!?;:\'"') in dictionary)
        ratio = meaningful / len(words)
        if ratio > best_ratio:
            best_ratio = ratio
            best_key = key
            best_decrypted = decrypted

    if best_key is not None and best_ratio > 0.3:
        return best_key, best_decrypted
    return None, None


def main():
    while True:
        print('\n' + '=' * 50)
        print('ШИФР ЦЕЗАРЯ — лабораторная работа 1')
        print('=' * 50)
        print('1. Зашифровать текст')
        print('2. Расшифровать текст')
        print('3. Атака по известному открытому тексту')
        print('4. Атака по шифрованному тексту (полный перебор)')
        print('5. Атака со словарём (автоопределение ключа)')
        print('0. Выход')
        choice = input('Выберите пункт: ').strip()

        if choice == '1':
            text = input('Введите текст для шифрования: ')
            key = int(input('Введите ключ (0-25): '))
            print('Зашифрованный текст:', caesar_encrypt(text, key))

        elif choice == '2':
            text = input('Введите текст для расшифровки: ')
            key = int(input('Введите ключ (0-25): '))
            print('Расшифрованный текст:', caesar_decrypt(text, key))

        elif choice == '3':
            plain = input('Введите открытый текст: ')
            cipher = input('Введите зашифрованный текст: ')
            key = known_plaintext_attack(plain, cipher)
            if key is not None:
                print(f'Найден ключ: {key}')
            else:
                print('Не удалось определить ключ')

        elif choice == '4':
            text = input('Введите зашифрованный текст: ')
            for key, decrypted in brute_force(text):
                print(f'Ключ {key:2d}: {decrypted}')

        elif choice == '5':
            text = input('Введите зашифрованный текст: ')
            key, decrypted = dictionary_attack(text)
            if key is not None:
                print(f'Найден ключ: {key}')
                print(f'Расшифрованный текст: {decrypted}')
            else:
                print('Не удалось определить ключ')

        elif choice == '0':
            break


if __name__ == '__main__':
    main()
