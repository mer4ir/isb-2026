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

    Raises:
        FileNotFoundError: Если файл не найден.
        json.JSONDecodeError: Если файл содержит некорректный JSON.
    """

    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    except FileNotFoundError as e:
        print(f'[-] Ошибка: файл конфигурации не найден {path} - {e}')
        raise
    
    except json.JSONDecodeError as e:
        print(f'[-] Ошибка: файл {path} содержит некорректный JSON - {e}')
        raise
    
    except PermissionError as e:
        print(f'[-] Ошибка: нет прав для чтения файла {path} - {e}')
        raise
    
    except Exception as e:
        print(f'[-] Непредвиденная ошибка при загрузке конфигурации: {e}')
        raise
