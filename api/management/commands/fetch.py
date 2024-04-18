from django.core.management.base import BaseCommand
from django.db.models import Sum
from django.conf import settings
from datetime import datetime, date
from api.models import User, Product, Payment, Deal, ServiceConfiguration
import requests

from api.utils import create_payments, create_deals, send_telegram_message

BRANCHES = settings.BRANCHES_ID


def error_handler(message: str):
    today = date.today()

    users = User.objects.filter(created_at__date=today).count()
    payments = Payment.objects.filter(created_at__date=today).count()
    deals = Deal.objects.filter(created_at__date=today).count()
    products = Product.objects.filter(created_at__date=today).count()

    main = (
        f"Технический отчет 📊\n\n"
        + f"📅 Дата: {today.strftime('%d/%m/%Y')}\n"
        + f"Создано пользователей: {users} шт\n"
        + f"Созданные платежи: {payments} шт\n"
        + f"Созданные сделки: {deals} шт\n"
        + f"Созданные товары: {products} шт\n\n"
        + f"Статус:\n{message} ❌"
    )

    send_telegram_message(main)


def success_handler(status: str):
    today = date.today()

    users = User.objects.filter(created_at__date=today)
    payments = Payment.objects.filter(created_at__date=today)
    deals = Deal.objects.filter(created_at__date=today)
    products = Product.objects.filter(created_at__date=today)

    message = (
        f"Технический отчет 📊\n\n"
        + f"📅  Дата: {today.strftime('%d/%m/%Y')}\n"
        + f"Созданные пользователи: {users.count()} шт\n"
        + f"Созданные платежи: {payments.count()} шт\n"
        + f"Созданные сделки: {deals.count()} шт\n"
        + f"Созданные товары: {products.count()} шт\n\n"
        + f"Статус:\n{status} ✅"
    )

    send_telegram_message(message)

    uzs_payments = payments.filter(payment_type__currency__name="Base SUM").aggregate(
        total_amount=Sum("amount")
    )["total_amount"]
    if not uzs_payments:
        uzs_payments = 0
    uzs_payments = round(uzs_payments, 2)

    usd_payments = payments.filter(payment_type__currency__name="USD").aggregate(
        total_amount=Sum("amount")
    )["total_amount"]
    if not usd_payments:
        usd_payments = 0
    usd_payments = round(usd_payments, 2)

    uzs_deals = deals.filter(payment_type__currency__name="Base SUM").aggregate(
        total_amount=Sum("total")
    )["total_amount"]
    if not uzs_deals:
        uzs_deals = 0
    uzs_deals = round(uzs_deals, 2)

    usd_deals = deals.filter(payment_type__currency__name="USD").aggregate(
        total_amount=Sum("total")
    )["total_amount"]
    if not usd_deals:
        usd_deals = 0
    usd_deals = round(usd_deals, 2)

    message = (
        f"Финансовый отчет 📊\n\n"
        + f"📅  Дата: {today.strftime('%d/%m/%Y')}\n\n"
        + f"Валюта: USD\n"
        + f"Сумма платежей: " + "{:,.2f}".format(usd_payments).replace(",", " ") + "\n"
        + f"Сумма сделок: " + "{:,.2f}".format(usd_deals).replace(",", " ") + "\n\n"
        + f"Валюта: UZS\n"
        + f"Сумма платежей: " + "{:,.2f}".format(uzs_payments).replace(",", " ") + "\n"
        + f"Сумма сделок: " + "{:,.2f}".format(uzs_deals).replace(",", " ") + "\n\n"
        + f"Статус:\n{status} ✅"
    )
    send_telegram_message(message)


def fetch_daily_data():
    service = ServiceConfiguration.objects.get(name="sync_daily_data")
    if not service.is_active:
        return

    date = datetime.now().strftime("%d.%m.%Y")

    for branch in BRANCHES:

        if not create_payments(branch, date):
            error_handler("Ошибка при создании платежей")
            return

        if not create_deals(branch, date):
            error_handler("Ошибка при создании сделок")
            return

    success_handler("Данные перенесены успешно")


class Command(BaseCommand):
    help = "Send message to customers who has payment for today"

    def handle(self, *args, **options):
        fetch_daily_data()
