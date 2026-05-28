import argparse

from keygen import generate_keys
from encrypt import encrypt_file
from decrypt import decrypt_file
from settings_loader import load_settings


def main():
    """
    Главная функция приложения.

    Выполняет:
    - обработку аргументов командной строки;
    - определение режима работы;
    - загрузку конфигурации;
    - запуск генерации ключей,
      шифрования или дешифрования.
    """

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '--generation',
        action='store_true',
        help='Режим генерации ключей'
    )

    group.add_argument(
        '--encryption',
        action='store_true',
        help='Режим шифрования'
    )

    group.add_argument(
        '--decryption',
        action='store_true',
        help='Режим дешифрования'
    )

    parser.add_argument(
        '--config',
        required=True,
        help='Путь к JSON-конфигу'
    )

    args = parser.parse_args()

    settings = load_settings(args.config)

    if args.generation:
        generate_keys(settings)

    elif args.encryption:
        encrypt_file(settings)

    elif args.decryption:
        decrypt_file(settings)


if __name__ == '__main__':
    main()