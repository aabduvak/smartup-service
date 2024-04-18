import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from django.conf import settings

from api.bot.commands.start import start
from api.bot.commands.workplaces import workplaces
from api.bot.commands.sms import sms_balance
from api.bot.commands.service_config import sms_service
from api.bot.commands.callback_query import callback_handler

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
CHAT_ID = settings.CHAT_ID

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)


def main():
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("workplaces", workplaces))
    dp.add_handler(CommandHandler("balance", sms_balance))
    dp.add_handler(CommandHandler("service", sms_service))
    dp.add_handler(CallbackQueryHandler(callback_handler))

    updater.start_polling()
    updater.idle()
