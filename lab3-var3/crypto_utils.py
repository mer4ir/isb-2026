import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


def generate_symmetric_key():
    """
    Генерирует случайный симметричный ключ длиной 256 бит
    для алгоритма шифрования ChaCha20.
    
    Для генерации используется криптографически стойкий
    генератор случайных чисел os.urandom().
    
    Returns:
        bytes: Случайный ключ длиной 32 байта.
    """
    return os.urandom(32)  # 256 бит


def generate_nonce():
    """
    Генерирует nonce (одноразовое случайное число)
    для алгоритма ChaCha20.
    
    Nonce используется для обеспечения уникальности
    процесса шифрования и предотвращения повторного
    использования одинаковых параметров.
    
    Returns:
        bytes: Случайный nonce длиной 16 байт.
    """
    return os.urandom(16)  # 128 бит


def encrypt_file_chacha20(data, key, nonce):
    """
    Выполняет шифрование данных алгоритмом ChaCha20.
    Функция создает объект шифра ChaCha20,
    инициализирует шифратор и выполняет
    преобразование исходных данных.
    
    Args:
        data (bytes):
            Исходные данные для шифрования.
        key (bytes):
            Симметричный ключ длиной 256 бит.
        nonce (bytes):
            Одноразовое случайное число длиной 128 бит.
            
    Returns:
        bytes:
            Зашифрованные данные.
    """
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(data)

    return encrypted_data


def decrypt_file_chacha20(data, key, nonce):
    """
    Выполняет дешифрование данных алгоритмом ChaCha20.
    Функция создает объект дешифратора и
    восстанавливает исходное содержимое файла.

    Args:
        data (bytes):
            Зашифрованные данные.
        key (bytes):
            Симметричный ключ длиной 256 бит.
        nonce (bytes):
            Nonce, использованный при шифровании.

    Returns:
        bytes:
            Расшифрованные данные.
    """
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(data)

    return decrypted_data


def generate_rsa_keys():
    """
    Генерирует пару RSA-ключей.

    Создается закрытый RSA-ключ длиной 2048 бит,
    после чего на его основе формируется
    соответствующий открытый ключ.

    Returns:
        tuple:
            Кортеж из двух элементов:
            - private_key — закрытый RSA-ключ;
            - public_key — открытый RSA-ключ.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    return private_key, public_key


def serialize_private_key(private_key, path):
    """
    Сериализует и сохраняет закрытый RSA-ключ в PEM-файл.

    Закрытый ключ сохраняется в формате TraditionalOpenSSL
    без дополнительного шифрования.

    Args:
        private_key:
            Объект закрытого RSA-ключа.
        path (str):
            Путь к файлу для сохранения ключа.
    """
    with open(path, 'wb') as file:
        file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )


def serialize_public_key(public_key, path):
    """
    Сериализует и сохраняет открытый RSA-ключ в PEM-файл.

    Args:
        public_key:
            Объект открытого RSA-ключа.
            
        path (str):
            Путь к файлу для сохранения ключа.
    """
    with open(path, 'wb') as file:
        file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


def load_private_key(path):
    """
    Загружает закрытый RSA-ключ из PEM-файла.

    Args:
        path (str):
            Путь к PEM-файлу закрытого ключа.

    Returns:
        RSAPrivateKey:
            Десериализованный объект закрытого RSA-ключа.
    """
    with open(path, 'rb') as file:
        data = file.read()

    return serialization.load_pem_private_key(
        data,
        password=None
    )


def load_public_key(path):
    """
    Загружает открытый RSA-ключ из PEM-файла.

    Args:
        path (str):
            Путь к PEM-файлу открытого ключа.

    Returns:
        RSAPublicKey:
            Десериализованный объект открытого RSA-ключа.
    """
    with open(path, 'rb') as file:
        data = file.read()

    return serialization.load_pem_public_key(data)

def encrypt_symmetric_key(sym_key, public_key):
    """
    Шифрует симметричный ключ с использованием RSA-OAEP.

    Для повышения криптографической стойкости
    применяется схема OAEP с хеш-функцией SHA-256.

    Args:
        sym_key (bytes):
            Симметричный ключ ChaCha20.

        public_key:
            Открытый RSA-ключ.

    Returns:
        bytes:
            Зашифрованный симметричный ключ.
    """
    encrypted_key = public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_key


def decrypt_symmetric_key(encrypted_key, private_key):
    """
    Выполняет расшифрование симметричного ключа
    при помощи закрытого RSA-ключа.

    Args:
        encrypted_key (bytes):
            Зашифрованный симметричный ключ.

        private_key:
            Закрытый RSA-ключ.

    Returns:
        bytes:
            Расшифрованный симметричный ключ.
    """
    decrypted_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_key