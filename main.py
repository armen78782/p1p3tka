import re
import requests
from phonenumbers import parse, is_valid_number, carrier, timezone
from bs4 import BeautifulSoup

class ZorgPhoneReaper:
    def __init__(self, phone):
        self.phone = phone
        self.data = {"name": "N/A", "soc_networks": []}

    def _vk_hunt(self):
        try:
            url = f"https://vk.com/search?c[q]={self.phone}&c[section]=people"
            req = requests.get(url, headers={"User-Agent": "ZORG-BOT/666"}).text
            soup = BeautifulSoup(req, "html.parser")
            name_tag = soup.find("a", class_="people_row")
            if name_tag:
                self.data["name"] = name_tag.get("title", "N/A")
                self.data["soc_networks"].append(f"VK: {url}")
        except Exception as e:
            pass

    def _telegram_scan(self):
        try:
            from telegram import Bot
            bot = Bot(token="7697165564:AAHxXcUcza9HELqT06iNn0OVbqlE8iUmIMU")
            user = bot.get_chat(chat_id=self.phone)
            self.data["soc_networks"].append(f"TG: @{user.username}")
        except:
            pass

    def _leak_check(self):
        try:
            resp = requests.post("https://leakcheck.io/api", data={"key": "FREE", "check": self.phone})
            if "found" in resp.text:
                self.data["leaks"] = resp.json().get("sources", [])
        except:
            pass

    def execute(self):
        if not is_valid_number(parse(self.phone)):
            return {"error": "НЕДЕЙСТВИТЕЛЬНЫЙ НОМЕР"}
        
        self._vk_hunt()
        self._telegram_scan()
        self._leak_check()
        
        return self.data

if __name__ == "__main__":
    phone = input("ВВЕДИТЕ НОМЕР (+7XXX...): ")
    reaper = ZorgPhoneReaper(phone)
    result = reaper.execute()
    print(f"""
[🔥] ZORG-REPORT ДЛЯ {phone}:
ИМЯ: {result.get('name', 'НЕ НАЙДЕНО')}
СОЦСЕТИ: {', '.join(result.get('soc_networks', []))}
УТЕЧКИ: {result.get('leaks', 'НЕТ ДОСТУПА К ТЕМНЫМ БАЗАМ')}
    """)
