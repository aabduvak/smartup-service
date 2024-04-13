from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from django.conf import settings

from api.bot.commands.start import start
from api.bot.commands.workplaces import workplaces, button
from api.bot.commands.sms import sms_balance

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
CHAT_ID = settings.CHAT_ID

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)


def main():
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("workplaces", workplaces))
    dp.add_handler(CommandHandler("balance", sms_balance))

    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()
