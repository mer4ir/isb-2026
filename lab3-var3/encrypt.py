from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

from file_manager import read_binary_file, write_binary_file


def encrypt_file(settings):
    """
    Выполняет шифрование файла
    гибридной криптосистемой.

    Args:
        settings (dict):
            Конфигурация приложения.
    """

    print('[+] Загрузка RSA ключа...')

    with open(settings['private_key'], 'rb') as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None
        )

    encrypted_key = read_binary_file(
        settings['symmetric_encrypted']
    )

    print('[+] Расшифрование симметричного ключа...')

    symmetric_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    nonce = read_binary_file(
        settings['nonce']
    )

    source_data = read_binary_file(
        settings['source_file']
    )

    print('[+] Шифрование файла...')

    cipher = Cipher(
        algorithms.ChaCha20(
            symmetric_key,
            nonce
        ),
        mode=None
    )

    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(source_data)

    write_binary_file(
        settings['encrypted_file'],
        encrypted_data
    )

    print('[+] Файл успешно зашифрован')