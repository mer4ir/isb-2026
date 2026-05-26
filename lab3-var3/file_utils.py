def write_binary_file(path, data):
    """
    Сохраняет бинарные данные в файл.

    Файл открывается в режиме бинарной записи.
    Если файл не существует, он будет создан.

    Args:
        path (str):
            Путь к сохраняемому файлу.

        data (bytes):
            Данные для записи.
    """
    with open(path, 'wb') as file:
        file.write(data)


def read_binary_file(path):
    """
    Считывает бинарные данные из файла.

    Args:
        path (str):
            Путь к считываемому файлу.

    Returns:
        bytes:
            Содержимое файла в виде массива байтов.
    """
    with open(path, 'rb') as file:
        return file.read()