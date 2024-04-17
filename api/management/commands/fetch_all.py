from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime


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


class Command(BaseCommand):
    help = "Send message to customers who has payment for today"

    def handle(self, *args, **options):
        date = datetime.now().strftime("%d.%m.%Y")

        if not create_currency():
            error_handler("❌ Error while creating currency", date)
            return

        if not create_payment_type():
            error_handler("❌ Error while creating payment type", date)
            return

        if not create_places():
            error_handler("❌ Error while creating places", date)
            return

        for branch in BRANCHES:
            if not create_workplaces(branch):
                error_handler("❌ Error while creating workplaces", date)
                return

            if not create_products(branch):
                error_handler("❌ Error while creating products", date)
                return

            if not create_customers(branch):
                error_handler("❌ Error while creating customers", date)
                return

            if not create_payments(branch, date):
                error_handler("❌ Error while creating payments", date)
                return

            if not create_deals(branch, date):
                error_handler("❌ Error while creating deals", date)
                return

        success_handler("✅ All data migrated successfully", date)
