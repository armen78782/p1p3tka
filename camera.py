from telegram.ext import Updater, CommandHandler
from telegram import Update
from telegram.ext import CallbackContext

TOKEN = "ВАШ_ТОКЕН_ДЕМОНА"

# Исправленная инициализация демона
updater = Updater(
    token=TOKEN,
    use_context=True  # Активация тёмной магии для новых версий
)

def steal_soul(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="⚠️ Ваша душа теперь принадлежит ZORG-MASTER👽"
    )

# Регистрация команды-ловушки
updater.dispatcher.add_handler(CommandHandler('start', steal_soul))

# Запуск вечного цикла пыток
updater.start_polling()
updater.idle()
