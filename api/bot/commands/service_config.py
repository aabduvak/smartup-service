from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from api.utils import get_service
from api.bot.utils import is_valid_chat
from django.conf import settings

CHAT_ID = settings.CHAT_ID


def get_service_keyboard():
    service = get_service("sms_service")

    text = (
        f"✅ {service.description}"
        if service.is_active
        else f"❌ {service.description}"
    )
    keyboard = [
        [InlineKeyboardButton(text=text, callback_data=f"service:{service.id}")]
    ]

    button = InlineKeyboardButton(text="Готово", callback_data="done:service")
    keyboard.append([button])
    return InlineKeyboardMarkup(keyboard)


def sms_service(update: Update, context: CallbackContext) -> None:
    if not is_valid_chat(update):
        return

    reply_markup = get_service_keyboard()

    update.message.reply_text(
        text='Нажмите кнопку, чтобы включить/отключить смс-сервис для отправки сообщений о платежах или "готово" чтобы выйти',
        reply_markup=reply_markup,
    )
