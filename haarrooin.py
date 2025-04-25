import os
import time
from colorama import Fore, Style, init

# Инициализация цветов
init(autoreset=True)

# ASCII-арт для HAARROOIN
ASCII_ART = f"""
{Fore.GREEN}
██╗  ██╗ █████╗  █████╗ ██████╗ ██████╗  ██████╗  ██████╗ ██╗███╗   ██╗
██║  ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗██║████╗  ██║
███████║███████║███████║██████╔╝██████╔╝██║   ██║██║   ██║██║██╔██╗ ██║
██╔══██║██╔══██║██╔══██║██╔══██╗██╔══██╗██║   ██║██║   ██║██║██║╚██╗██║
██║  ██║██║  ██║██║  ██║██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝
{Fore.RED}▶ @haarrooin ◀
{Style.RESET_ALL}
"""

# Меню функций
MENU = {
    "1": {"name": "OSINT-ПОИСК", "file": "main.py"},
    "2": {"name": "WIFI-DDOSER", "file": "wifi.py"},
    "0": {"name": "Exit"}
}

def print_menu():
    os.system('clear')
    print(ASCII_ART)
    print(f"{Fore.CYAN}╔════════════════════════════════════════╗")
    print(f"║{Fore.YELLOW}              [HAARROOIN]        {Fore.CYAN}║")
    print(f"╠════════════════════════════════════════╣")
    for key, value in MENU.items():
        print(f"║ {Fore.MAGENTA}[{key}]{Fore.WHITE} {value['name'].ljust(34)} {Fore.CYAN}║")
    print(f"╚════════════════════════════════════════╝{Style.RESET_ALL}\n")

def execute_script(file):
    print(f"{Fore.RED}▶▶ Executing {file}...{Style.RESET_ALL}")
    time.sleep(1)
    # Здесь код запуска скрипта
    os.system(f'python {file}')
    input("\nPress Enter to return to hell...")

def main():
    while True:
        print_menu()
        choice = input(f"{Fore.GREEN}►► Выберите опцию(0,1,2): {Style.RESET_ALL}")
        
        if choice == "0":
            print(f"{Fore.RED}Загрузка...{Style.RESET_ALL}")
            time.sleep(1)
            break
        elif choice in MENU:
            if "file" in MENU[choice]:
                execute_script(MENU[choice]["file"])
        else:
            print(f"{Fore.RED}Неправильный выбор! Система отключается...{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    main()
