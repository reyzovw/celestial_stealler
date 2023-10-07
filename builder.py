import subprocess
import os
import traceback

with open(os.devnull, 'w') as fnull:
    try:
        from colorama import init, Fore
    except ModuleNotFoundError:
        subprocess.call(['pip', 'install', 'colorama'], stdout=fnull, stderr=fnull)


print(Fore.RED + """
            ███████████████████████████████████████████████████████████████████████████████████████████
            █─▄▄▄▄█─█─█▄─▄▄─█▄─▄▄▀█▄─▄▄─█▄─▄─▀█▄─▄▄─█─▄▄─█─▄▄▄─█─▄─▄─█▄─▄▄─█─█─█▄─▄▄▀█─▄▄─█▄─▄▄─█▄─▄▄─█
            █▄▄▄▄─█─▄─██─▄█▀██─██─██─▄█▀██─▄─▀██─▄▄▄█─██─█─███▀███─████─▄█▀█─▄─██─██─█─██─██─▄████─▄███
            ▀▄▄▄▄▄▀▄▀▄▀▄▄▄▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀▄▄▄▄▀▀▄▄▄▀▀▀▄▄▄▄▀▄▄▄▄▄▀▀▄▄▄▀▀▄▄▄▄▄▀▄▀▄▀▄▄▄▄▀▀▄▄▄▄▀▄▄▄▀▀▀▄▄▄▀▀▀
    """ + Fore.RESET)

try:
    os.system(f'pyinstaller --onefile main.py')
    try:
        import PyInstaller
    except ImportError:
        print(f"{Fore.RED}PyInstaller не установлен. Устанавливаю PyInstaller...{Fore.RESET}")
        with open(os.devnull, 'w') as fnull:
            subprocess.call(['pip', 'install', 'pyinstaller'], stdout=fnull, stderr=fnull)
        print(f"{Fore.GREEN}Установка PyInstaller завершена{Fore.RESET}")
    
    try:
        os.system(f'pyinstaller --onefile main.py')
    except Exception as e:
        print(e)
        subprocess.call(['-m', 'pip', 'uninstall', 'pathlib'], stdout=fnull, stderr=fnull)
    print(f'{Fore.GREEN}Файл успешно скомпилирован{Fore.RESET}')
except Exception as e:
    print(f'{Fore.RED}Ошибка при компиляции: {e}{Fore.RESET}')