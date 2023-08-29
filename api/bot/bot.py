from api.utils import get_workplace_list, toggle_workplace, get_debt_list
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from django.conf import settings

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
CHAT_ID = settings.CHAT_ID

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"Group Chat ID: {update.message.chat_id}")




def debt(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id != int(CHAT_ID):
        update.message.reply_text(text=f"🚫 У вас недостаточно прав для запуска этой команды")
        return
    
    keyboard = []
    for place in workplaces:
        name = f'❌ {place.name}'
        if place.is_active:
            name = f'✅ {place.name}'

        button = InlineKeyboardButton(text=name, callback_data=str(place.id))

        keyboard.append([button])

    button = InlineKeyboardButton(text="Готово", callback_data="done")
    keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text="Список рабочих мест\nНажмите кнопку, чтобы включить/отключить отправку сообщений клиентам на соответствующем рабочем месте или нажмите \"готово\" чтобы выйти", reply_markup=reply_markup)



def get_keyboard():
    workplaces = get_workplace_list()
    keyboard = []
    for place in workplaces:
        name = f'❌ {place.name}'
        if place.is_active:
            name = f'✅ {place.name}'

        button = InlineKeyboardButton(text=name, callback_data=str(place.id))

        keyboard.append([button])

    button = InlineKeyboardButton(text="Готово", callback_data="done")
    keyboard.append([button])
    return keyboard


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    workplace_id = query.data

    if workplace_id == 'done':
        query.message.delete()
        return

    if not toggle_workplace(workplace_id):
        query.answer(text="⚠️ Невозможно переключить рабочее место")

    new_keyboard = get_keyboard()
    new_markup = InlineKeyboardMarkup(new_keyboard)
    query.edit_message_text(text="Обновленные рабочие места\nнажмите \"готово\" чтобы выйти", reply_markup=new_markup)

    query.answer(text="✅ Рабочее место успешно переключился")

def workplaces(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id != int(CHAT_ID):
        update.message.reply_text(text=f"🚫 У вас недостаточно прав для запуска этой команды")
        return
    keyboard = get_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text="Список рабочих мест\nНажмите кнопку, чтобы включить/отключить отправку сообщений клиентам на соответствующем рабочем месте или нажмите \"готово\" чтобы выйти", reply_markup=reply_markup)

def main():
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("workplaces", workplaces))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()