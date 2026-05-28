import json


def load_settings(path):
    """
    Загружает JSON-конфигурацию приложения.

    Args:
        path (str):
            Путь к JSON-файлу.

    Returns:
        dict:
            Словарь с настройками приложения.
    """

    with open(path, 'r') as file:
        return json.load(file)