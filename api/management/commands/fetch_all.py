from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime

from api.models import ServiceConfiguration
from api.utils import (
    create_currency,
    create_payment_type,
    create_places,
    create_customers,
    create_products,
    create_payments,
    create_deals,
    create_workplaces,
    send_telegram_message,
)

BRANCHES = settings.BRANCHES_ID
TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
CHAT_ID = settings.CHAT_ID


def error_handler(message: str, date: datetime):
    send_telegram_message(message)


def success_handler(message: str, date: datetime):
    send_telegram_message(message)


def fetch_all_data():
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

    if not create_places():
        error_handler("❌ Ошибка при создании мест.", date)
        return

    for branch in BRANCHES:
        if not create_workplaces(branch):
            error_handler("❌ Ошибка при создании рабочих мест", date)
            return

        if not create_products(branch):
            error_handler("❌ Ошибка при создании товаров", date)
            return

        if not create_customers(branch):
            error_handler("❌ Ошибка при создании клиентов", date)
            return

        if not create_payments(branch, date):
            error_handler("❌ Ошибка при создании платежей", date)
            return

        if not create_deals(branch, date):
            error_handler("❌ Ошибка при создании сделок", date)
            return

    success_handler("✅ Все данные успешно перенесены", date)


class Command(BaseCommand):
    help = "Fetch all data from Smartup API"

    def handle(self, *args, **options):
        fetch_all_data()
