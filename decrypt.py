import os
import pyAesCrypt


def decrypt_file(file, password):
    """
    Расшифровывает файл с использованием pyAesCrypt.

    :param file: Путь к зашифрованному файлу.
    :param password: Пароль для расшифрования.
    """
    bufferSize = 512 * 1024
    output_file = file[:-4]  # Убираем расширение .crp
    try:
        pyAesCrypt.decryptFile(file, output_file, password, bufferSize)
        os.remove(file)  # Удаляем зашифрованный файл после расшифрования
        print(f"Файл {file} успешно расшифрован.")
    except ValueError:
        print(f"Неверный пароль для файла {file}. Расшифрование не удалось.")


def walk_and_decrypt(dir, password):
    """
    Рекурсивно проходит по директории и расшифровывает все файлы с расширением .crp.

    :param dir: Путь к директории.
    :param password: Пароль для расшифрования.
    """
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path) and path.endswith(".crp"):
            decrypt_file(path, password)
        elif os.path.isdir(path):
            walk_and_decrypt(path, password)


if __name__ == "__main__":
    # Укажите директорию с зашифрованными файлами
    direct = r"C:\test"

    # Запрос пароля у пользователя
    decrypt_pass = input("Введите пароль для расшифрования: ")

    # Расшифровка файлов в указанной директории
    walk_and_decrypt(direct, decrypt_pass)
