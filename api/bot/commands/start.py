from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    message = f"Привет {update.effective_user.full_name}\nID этого чата: {update.message.chat_id}"
    update.message.reply_text(message)
