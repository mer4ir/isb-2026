import json
import argparse

from crypto_utils import *
from file_utils import *


def load_config(path):

    with open(path, 'r') as file:
        return json.load(file)

def generate_keys(config):

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