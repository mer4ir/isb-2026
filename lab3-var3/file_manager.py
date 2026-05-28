def write_binary_file(path, data):
    """
    Сохраняет бинарные данные в файл.

    Args:
        path (str):
            Путь к файлу.

        data (bytes):
            Бинарные данные.
    """

    with open(path, 'wb') as file:
        file.write(data)


def read_binary_file(path):
    """
    Считывает бинарные данные из файла.

    Args:
        path (str):
            Путь к файлу.

    Returns:
        bytes:
            Содержимое файла.
    """

    with open(path, 'rb') as file:
        return file.read()