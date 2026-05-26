import json
import argparse

from crypto_utils import *
from file_utils import *


def load_config(path):
    """
    Загружает JSON-конфигурацию приложения.

    Конфигурационный файл содержит пути
    ко всем используемым файлам:
    ключам, nonce, исходным и
    зашифрованным данным.

    Args:
        path (str):
            Путь к JSON-файлу конфигурации.

    Returns:
        dict:
            Словарь с параметрами конфигурации.
    """
    with open(path, 'r') as file:
        return json.load(file)

def generate_keys(config):
    """
    Выполняет режим генерации ключей
    гибридной криптосистемы.

    В процессе работы:
    1. Генерируется симметричный ключ ChaCha20;
    2. Генерируется nonce;
    3. Создается пара RSA-ключей;
    4. RSA-ключи сохраняются в файлы;
    5. Симметричный ключ шифруется RSA;
    6. Зашифрованный ключ сохраняется на диск.

    Args:
        config (dict):
            Конфигурация приложения.
    """
    print("[+] Генерация симметричного ключа...")

    sym_key = generate_symmetric_key()

    print("[+] Генерация nonce...")

    nonce = generate_nonce()

    print("[+] Генерация RSA ключей...")

    private_key, public_key = generate_rsa_keys()

    print("[+] Сериализация RSA ключей...")

    serialize_private_key(
        private_key,
        config["private_key"]
    )

    serialize_public_key(
        public_key,
        config["public_key"]
    )

    print("[+] Шифрование симметричного ключа RSA...")

    encrypted_sym_key = encrypt_symmetric_key(
        sym_key,
        public_key
    )

    write_binary_file(
        config["encrypted_symmetric_key"],
        encrypted_sym_key
    )

    write_binary_file(
        config["nonce"],
        nonce
    )

    print("[+] Ключи успешно созданы")
    

def encrypt_data(config):
    """
    Выполняет шифрование файла
    гибридной криптосистемой.

    Функция:
    1. Загружает RSA-закрытый ключ;
    2. Расшифровывает симметричный ключ;
    3. Загружает nonce;
    4. Считывает исходный файл;
    5. Шифрует данные алгоритмом ChaCha20;
    6. Сохраняет результат в файл.

    Args:
        config (dict):
            Конфигурация приложения.
    """
    print("[+] Загрузка приватного RSA ключа...")

    private_key = load_private_key(
        config["private_key"]
    )

    print("[+] Загрузка зашифрованного симметричного ключа...")

    encrypted_sym_key = read_binary_file(
        config["encrypted_symmetric_key"]
    )

    print("[+] Расшифрование симметричного ключа...")

    sym_key = decrypt_symmetric_key(
        encrypted_sym_key,
        private_key
    )

    nonce = read_binary_file(
        config["nonce"]
    )

    print("[+] Чтение исходного файла...")

    data = read_binary_file(
        config["input_file"]
    )

    print("[+] Шифрование данных ChaCha20...")

    encrypted_data = encrypt_file_chacha20(
        data,
        sym_key,
        nonce
    )

    write_binary_file(
        config["encrypted_file"],
        encrypted_data
    )

    print("[+] Файл успешно зашифрован")
    

def decrypt_data(config):
    """
    Выполняет дешифрование файла
    гибридной криптосистемой.

    Функция:
    1. Загружает RSA-закрытый ключ;
    2. Расшифровывает симметричный ключ;
    3. Загружает nonce;
    4. Считывает зашифрованный файл;
    5. Выполняет дешифрование ChaCha20;
    6. Сохраняет исходные данные.

    Args:
        config (dict):
            Конфигурация приложения.
    """
    print("[+] Загрузка приватного RSA ключа...")

    private_key = load_private_key(
        config["private_key"]
    )

    encrypted_sym_key = read_binary_file(
        config["encrypted_symmetric_key"]
    )

    print("[+] Расшифрование симметричного ключа...")

    sym_key = decrypt_symmetric_key(
        encrypted_sym_key,
        private_key
    )

    nonce = read_binary_file(
        config["nonce"]
    )

    encrypted_data = read_binary_file(
        config["encrypted_file"]
    )

    print("[+] Дешифрование данных...")

    decrypted_data = decrypt_file_chacha20(
        encrypted_data,
        sym_key,
        nonce
    )

    write_binary_file(
        config["decrypted_file"],
        decrypted_data
    )

    print("[+] Файл успешно расшифрован")


def main():
    """
    Главная функция приложения.

    Выполняет:
    - обработку аргументов командной строки;
    - определение выбранного режима работы;
    - загрузку конфигурации;
    - запуск соответствующего сценария:
      генерации ключей, шифрования
      или дешифрования данных.
    """
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(
        required=True
    )

    group.add_argument(
        '--generation',
        action='store_true'
    )

    group.add_argument(
        '--encryption',
        action='store_true'
    )

    group.add_argument(
        '--decryption',
        action='store_true'
    )

    parser.add_argument(
        '--config',
        required=True
    )

    args = parser.parse_args()

    config = load_config(args.config)

    if args.generation:
        generate_keys(config)

    elif args.encryption:
        encrypt_data(config)

    elif args.decryption:
        decrypt_data(config)


if __name__ == '__main__':
    main()