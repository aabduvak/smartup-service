from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from api.utils import get_workplace_list
from api.bot.utils import is_valid_chat
from django.conf import settings

CHAT_ID = settings.CHAT_ID


def get_workplaces_keyboard():
    workplaces = get_workplace_list()

    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{'✅' if place.is_active else '❌'} {place.name}",
                callback_data=f"workplace:{place.id}",
            )
        ]
        for place in workplaces
    ]

    done_button = InlineKeyboardButton(text="Готово", callback_data="done:workplace")
    keyboard.append([done_button])

    return InlineKeyboardMarkup(keyboard)


def workplaces(update: Update, context: CallbackContext) -> None:
    if not is_valid_chat(update):
        return

    reply_markup = get_workplaces_keyboard()

    update.message.reply_text(
        text='Список рабочих мест\nНажмите кнопку, чтобы включить/отключить отправку сообщений клиентам на соответствующем рабочем месте или нажмите "готово" чтобы выйти',
        reply_markup=reply_markup,
    )
