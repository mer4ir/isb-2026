from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

from key_loader import load_private_key
from file_manager import read_binary_file, write_binary_file


def decrypt_file(settings):
    """
    Выполняет дешифрование файла
    гибридной криптосистемой.

    Args:
        settings (dict):
            Конфигурация приложения.
    """

    print('[+] Загрузка RSA ключа...')

    private_key = load_private_key(settings)

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

    encrypted_data = read_binary_file(
        settings['encrypted_file']
    )

    print('[+] Дешифрование файла...')

    cipher = Cipher(
        algorithms.ChaCha20(
            symmetric_key,
            nonce
        ),
        mode=None
    )

    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(
        encrypted_data
    )

    write_binary_file(
        settings['decrypted_file'],
        decrypted_data
    )

    print('[+] Файл успешно расшифрован')