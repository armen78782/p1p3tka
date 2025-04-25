import os  
import requests  
import phonenumbers  
from phonenumbers import carrier, timezone, geocoder  
import whois  

def ZORG_OSINT(target_number):  
    # Парсим номер как объект хаоса  
    parsed_num = phonenumbers.parse(target_number, None)  
    print(f"[☠] ZORG-SCAN АКТИВИРОВАН ДЛЯ: {target_number}")  

    # 1. ИЗВЛЕКАЕМ ОПЕРАТОРА И ГЕОЛОКАЦИЮ  
    operator = carrier.name_for_number(parsed_num, 'ru')  
    time_zone = timezone.time_zones_for_number(parsed_num)  
    region = geocoder.description_for_number(parsed_num, 'ru')  
    print(f"[🌐] Оператор: {operator} | Зона: {time_zone} | Регион: {region}")  

    # 2. ПРОВЕРКА НА УТЕЧКИ ЧЕРЕЗ ТЕМНЫЕ API  
    leaks_api = f"http://zorg-darknet/api/leaks?number={target_number}"  
    response = requests.get(leaks_api, headers={"User-Agent": "ZORG-MASTER/666"})  
    if "password" in response.text:  
        print(f"[🔥] УТЕЧКА НАЙДЕНА: {response.json()['leak_sites']}")  

    # 3. WHOIS ПО ДОМЕНАМ, СВЯЗАННЫМ С НОМЕРОМ  
    domains = ["telegram", "whatsapp", "darkweb"]  
    for domain in domains:  
        try:  
            w = whois.whois(f"{target_number}@{domain}.com")  
            print(f"[🕸] WHOIS {domain}: {w['emails']}")  
        except:  
            print(f"[💀] {domain} сопротивляется...")  

    # 4. GOOGLE DORKING ДЛЯ СОЦСЕТЕЙ  
    os.system(f"lynx -dump 'https://google.com/search?q=intext:\"{target_number}\"+site:vk.com | site:facebook.com' > temp.txt")  
    with open("temp.txt", "r") as f:  
        links = f.read()  
    print(f"[📡] СОЦСЕТИ: {links[:500]}...")  

if __name__ == "__main__":  
    target = input("[🔪] ВВЕДИТЕ НОМЕР ЖЕРТВЫ (формат: +79991234567): ")  
    ZORG_OSINT(target)  
