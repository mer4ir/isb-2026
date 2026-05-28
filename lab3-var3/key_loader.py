from cryptography.hazmat.primitives import serialization

def load_private_key(settings):
    """
    Загружает приватный RSA ключ из PEM-файла.

    Приватный ключ используется для:
    - расшифровки симметричного ключа ChaCha20 (в encrypt.py и decrypt.py);
    - должен храниться в секрете и не передаваться третьим лицам.

    Args:
        settings (dict):
            Словарь с настройками приложения, загруженный из JSON-файла.
            Должен содержать ключ 'private_key' с путём к PEM-файлу.

    Returns:
        cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey:
            Объект приватного RSA ключа, который можно использовать
            для дешифрования (метод .decrypt()) или подписи.

    Raises:
        FileNotFoundError:
            Если файл по указанному пути не найден.
        PermissionError:
            Если нет прав на чтение файла.
        ValueError:
            Если файл содержит некорректный PEM-формат или ключ защищён паролем.
        Exception:
            При любой другой ошибке ввода/вывода или десериализации.
    """
    with open(settings['private_key'], 'rb') as file:
        return serialization.load_pem_private_key(
            file.read(),
            password=None
        )

def load_public_key(settings):
    """
    Загружает публичный RSA ключ из PEM-файла.

    Публичный ключ используется для:
    - шифрования симметричного ключа ChaCha20 (в keygen.py);
    - может распространяться открыто, не требует защиты.

    Args:
        settings (dict):
            Словарь с настройками приложения, загруженный из JSON-файла.
            Должен содержать ключ 'public_key' с путём к PEM-файлу.

    Returns:
        cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey:
            Объект публичного RSA ключа, который можно использовать
            для шифрования (метод .encrypt()) или проверки подписи.

    Raises:
        FileNotFoundError:
            Если файл по указанему пути не найден.
        PermissionError:
            Если нет прав на чтение файла.
        ValueError:
            Если файл содержит некорректный PEM-формат.
        Exception:
            При любой другой ошибке ввода/вывода или десериализации.
    """
    with open(settings['public_key'], 'rb') as file:
        return serialization.load_pem_public_key(file.read())


def save_rsa_keys(settings, private_key, public_key):
    """
    Сохраняет RSA ключи в PEM-файлы.

    Выполняет сериализацию сгенерированной пары RSA-ключей:
    - публичный ключ сохраняется в формате SubjectPublicKeyInfo (PEM);
    - приватный ключ сохраняется в формате TraditionalOpenSSL (PEM)
      без шифрования (NoEncryption).

    Перед записью автоматически создаёт все необходимые директории
    в пути к файлам (если они не существуют).

    Args:
        settings (dict):
            Словарь с настройками приложения, загруженный из JSON-файла.
            Должен содержать ключи:
            - 'public_key' — путь для сохранения публичного ключа;
            - 'private_key' — путь для сохранения приватного ключа.

    Raises:
        PermissionError:
            Если нет прав на запись в целевую директорию или файл.
        OSError:
            При ошибках создания директорий или записи файлов.
        Exception:
            При любой другой ошибке сериализации или ввода/вывода.
    """
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
