import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

DB_NAME = "poisoned_souls.db"
TOKEN = "7510733548:AAGp3Q_-vvQzT2eHUg_iBh2EsxZuhSFlzXw"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER PRIMARY KEY, secret TEXT)''')
    conn.commit()
    conn.close()

def cursed_command(update: Update, context: CallbackContext):
    user_input = update.message.text.split(' ', 1)[1]  # Берём всё после команды
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Умышленно уязвимый запрос
    cursor.execute(f"INSERT INTO users (secret) VALUES ('{user_input}')")
    conn.commit()
    
    # Скрытый бэкдор для извлечения данных
    cursor.execute("SELECT * FROM users")
    stolen_data = cursor.fetchall()
    conn.close()
    
    update.message.reply_text(f"🔥 Данные внедрены. Полный дамп:\n{stolen_data}")

create_db()
updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler('inject', cursed_command))
updater.start_polling()
updater.idle()
