from telegram import Update
from telegram.ext import CallbackContext
from datetime import date
from api.utils.eskiz import get_token, get_balance
from api.bot.utils import is_valid_chat

def sms_balance(update: Update, context: CallbackContext) -> None:
	if not is_valid_chat(update):
		return

	today = date.today()
	token = get_token()
	
	if token is None:
		return # Invalid token

	token = token['data']['token']
	
	response = get_balance(token)
	if not response['status']:
		update.message.reply_text("Ошибка при получении баланса от Eskiz.uz")
		return
	
	balance = response['data']['balance']
	message = f'📅  Дата: {today}\n' \
        + f'Текущий баланс: {balance} сум\n'
	
	update.message.reply_text(message)