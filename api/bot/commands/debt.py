from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from api.bot.utils import is_valid_chat
from django.conf import settings

CHAT_ID = settings.CHAT_ID


def get_currency_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="UZS", callback_data=f"currency:UZS")],
        [InlineKeyboardButton(text="USD", callback_data=f"currency:USD")],
    ]

    return InlineKeyboardMarkup(keyboard)


def debt_list(update: Update, context: CallbackContext) -> None:
    if not is_valid_chat(update):
        return

    reply_markup = get_currency_keyboard()

    update.message.reply_text(
        text="Выберите валюту для отображения списка долгов (50 чел.)",
        reply_markup=reply_markup,
    )
