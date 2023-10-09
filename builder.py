import subprocess
import os
from time import sleep

print("""\033[0;31m
██████╗    ░██╗░░░██╗   ██╗     ██╗░░░░░    ██████╗     ░███████╗   ██████╗░
██╔══██╗    ██║░░░██║   ██║     ██║░░░░░    ██╔══██╗    ██╔════╝    ██╔══██╗
██████╦╝    ██║░░░██║   ██║     ██║░░░░░    ██║░░██║    █████╗░░    ██████╔╝
██╔══██╗    ██║░░░██║   ██║     ██║░░░░░    ██║░░██║    ██╔══╝░░    ██╔══██╗
██████╦╝    ╚██████╔╝   ██║     ███████╗    ██████╔╝    ███████╗    ██║░░██║
╚═════╝░░    ╚═════╝░   ╚═╝     ╚══════╝    ╚═════╝     ░╚══════╝   ╚═╝░░╚═╝
\033[0m""")

sleep(1)

try:
    os.system("pyinstaller --onefile main.py")
    try:
        import PyInstaller
    except:
        print('Устанавливаю нужные библиотеки, пожалуйста подождите...')
        with open(os.devnull, 'w') as fnull:
            subprocess.call(['pip', 'install', 'pyinstaller'], stdout=fnull, stderr=fnull)
        print("Библиотеки успешно установленны")
        try:
            os.system("pyinstaller --onefile main.py")
        except Exception as e:
            print(f'Произошла ошибка: {e}')
            sleep(1)
            print('Пожалуйста подождите, программа пытается исправить ее...')
            with open(os.devnull, 'w') as fnull:
                subprocess.call(['-m', 'pip', 'uninstall', 'pathlib'], stdout=fnull, stderr=fnull)
            try:
                os.system("pyinstaller --onefile main.py")
                print('Пытаемся собрать файл после попытки исправления ошибка...')
            except Exception as exp:
                sleep(1)
                print(f'Ошибка не исправилась, ошибка: {exp}')
    print('Сборка успешно завершилась, ваш .exe файл хранится по директории dist/main.py')
except Exception as tryexp:
    print(f'Ошибка при запуске: {exp}')