from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from django.conf import settings

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

def start(update: Update, context: CallbackContext) -> None:
    # Send a message to the user with the chat ID of the group
    update.message.reply_text(f"Group Chat ID: {update.message.chat_id}")

def main():
    dp = updater.dispatcher

    # Command to trigger the start function
    dp.add_handler(CommandHandler("start", start))

    # Start the bot
    updater.start_polling()
    updater.idle()