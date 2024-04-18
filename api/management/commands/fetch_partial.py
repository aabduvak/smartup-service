from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime

from api.models import ServiceConfiguration
from api.utils import (
    create_currency,
    create_payment_type,
    create_places,
    send_telegram_message,
)

BRANCHES = settings.BRANCHES_ID
TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
CHAT_ID = settings.CHAT_ID


def error_handler(message: str, date: datetime):
    send_telegram_message(message)


def fetch_partial_data():
    service = ServiceConfiguration.objects.get(name="sync_daily_data")
    if not service.is_active:
        return

    date = datetime.now().strftime("%d.%m.%Y")

    if not create_currency():
        error_handler("❌ Ошибка при создании валюты", date)
        return

    if not create_payment_type():
        error_handler("❌ Ошибка при создании типа платежа", date)
        return

class Command(BaseCommand):
    help = "Fetch partial data from Smartup API"

    def handle(self, *args, **options):
        fetch_partial_data()
