import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

def generate_symmetric_key():
    return os.urandom(32)  # 256 бит


def generate_nonce():
    return os.urandom(16)  # 128 бит


def encrypt_file_chacha20(data, key, nonce):
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(data)

    return encrypted_data


def decrypt_file_chacha20(data, key, nonce):
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(data)

    return decrypted_data


def generate_rsa_keys():

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    return private_key, public_key


def serialize_private_key(private_key, path):

    with open(path, 'wb') as file:
        file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )


def serialize_public_key(public_key, path):

    with open(path, 'wb') as file:
        file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


def load_private_key(path):

    with open(path, 'rb') as file:
        data = file.read()

    return serialization.load_pem_private_key(
        data,
        password=None
    )


def load_public_key(path):

    with open(path, 'rb') as file:
        data = file.read()

    return serialization.load_pem_public_key(data)

def encrypt_symmetric_key(sym_key, public_key):

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