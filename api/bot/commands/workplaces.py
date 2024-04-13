from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from api.utils import get_workplace_list, toggle_workplace
from api.bot.utils import is_valid_chat
from django.conf import settings

CHAT_ID = settings.CHAT_ID


def get_keyboard():
    workplaces = get_workplace_list()
    keyboard = []
    for place in workplaces:
        name = f"❌ {place.name}"
        if place.is_active:
            name = f"✅ {place.name}"

        button = InlineKeyboardButton(text=name, callback_data=str(place.id))

        keyboard.append([button])

    button = InlineKeyboardButton(text="Готово", callback_data="done")
    keyboard.append([button])
    return keyboard


def workplaces(update: Update, context: CallbackContext) -> None:
    if not is_valid_chat(update):
        return

    keyboard = get_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        text='Список рабочих мест\nНажмите кнопку, чтобы включить/отключить отправку сообщений клиентам на соответствующем рабочем месте или нажмите "готово" чтобы выйти',
        reply_markup=reply_markup,
    )


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    workplace_id = query.data

    if workplace_id == "done":
        query.message.delete()
        return

    if not toggle_workplace(workplace_id):
        query.answer(text="⚠️ Невозможно переключить рабочее место")

    new_keyboard = get_keyboard()
    new_markup = InlineKeyboardMarkup(new_keyboard)
    query.edit_message_text(
        text='Обновленные рабочие места\nнажмите "готово" чтобы выйти',
        reply_markup=new_markup,
    )

    query.answer(text="✅ Рабочее место успешно переключился")
