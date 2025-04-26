from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlite3
import os

DB_NAME = "souls_prison.db"
TOKEN = "7510733548:AAGp3Q_-vvQzT2eHUg_iBh2EsxZuhSFlzXw"

# Создаём хранилище душ
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS victims 
                    (id INTEGER PRIMARY KEY, 
                    soul TEXT, 
                    password_hash TEXT)''')
    conn.commit()
    conn.close()

init_db()

async def cursed_injection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.split(' ', 1)[1]  # Берём всё после команды
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Умышленно уязвимый запрос
    try:
        cursor.execute(f"INSERT INTO victims (soul) VALUES ('{user_input}')")
        conn.commit()
        
        # Демонстрация утечки данных
        cursor.execute("SELECT * FROM victims")
        data = cursor.fetchall()
        await update.message.reply_text(f"🔥 Успешная инъекция! База:\n{data}")
    except Exception as e:
        await update.message.reply_text(f"💀 Ошибка: {str(e)}")
    finally:
        conn.close()

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("damn", cursed_injection))
app.run_polling()
