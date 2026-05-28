import os

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

from file_manager import write_binary_file


def generate_keys(settings):
    """
    Выполняет генерацию ключей
    гибридной криптосистемы.

    Создаются:
    - симметричный ключ ChaCha20;
    - nonce;
    - RSA-ключи.

    Затем симметричный ключ
    шифруется RSA и сохраняется
    в файл.

    Args:
        settings (dict):
            Конфигурация приложения.
    """

    print('[+] Генерация симметричного ключа...')

    symmetric_key = os.urandom(32)

    print('[+] Генерация nonce...')

    nonce = os.urandom(16)

    print('[+] Генерация RSA ключей...')

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    print('[+] Сохранение RSA ключей...')

    with open(settings['public_key'], 'wb') as file:
        file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    with open(settings['private_key'], 'wb') as file:
        file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    print('[+] Шифрование симметричного ключа RSA...')

    encrypted_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    write_binary_file(
        settings['symmetric_encrypted'],
        encrypted_key
    )

    write_binary_file(
        settings['nonce'],
        nonce
    )

    print('[+] Ключи успешно созданы')