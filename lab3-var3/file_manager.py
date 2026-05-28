import os


def write_binary_file(path, data):
    """
    Сохраняет бинарные данные в файл.

    Args:
        path (str):
            Путь к файлу.

        data (bytes):
            Бинарные данные.

    Raises:
        IOError: Если не удалось записать файл.
    """

    try:
        # Создаём директорию, если её нет
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'wb') as file:
            file.write(data)
        print(f'[+] Файл успешно сохранён: {path}')
    
    except FileNotFoundError as e:
        print(f'[-] Ошибка: директория не найдена - {e}')
        raise
    
    except PermissionError as e:
        print(f'[-] Ошибка: нет прав для записи в файл {path} - {e}')
        raise
    
    except Exception as e:
        print(f'[-] Непредвиденная ошибка при записи файла {path}: {e}')
        raise


def read_binary_file(path):
    """
    Считывает бинарные данные из файла.

    Args:
        path (str):
            Путь к файлу.

    Returns:
        bytes:
            Содержимое файла.

    Raises:
        FileNotFoundError: Если файл не найден.
        IOError: Если не удалось прочитать файл.
    """

    try:
        with open(path, 'rb') as file:
            data = file.read()
        print(f'[+] Файл успешно прочитан: {path}')
        return data
    
    except FileNotFoundError as e:
        print(f'[-] Ошибка: файл не найден {path} - {e}')
        raise
    
    except PermissionError as e:
        print(f'[-] Ошибка: нет прав для чтения файла {path} - {e}')
        raise
    
    except Exception as e:
        print(f'[-] Непредвиденная ошибка при чтении файла {path}: {e}')
        raise