import requests
from django.conf import settings
from telegram import Update

CHAT_ID = settings.CHAT_ID
ESKIZ_EMAIL = settings.ESKIZ_EMAIL
ESKIZ_PASSWORD = settings.ESKIZ_PASSWORD
ESKIZ_URL = settings.ESKIZ_URL
BRANCHES_ID = settings.BRANCHES_ID

def is_valid_chat(update: Update):
	if update.message.chat_id != int(CHAT_ID):
		update.message.reply_text(text=f"🚫 У вас недостаточно прав для запуска этой команды")
		return False
	return True

