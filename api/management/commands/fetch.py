from django.core.management.base import BaseCommand
from django.db.models import Sum
from django.conf import settings
from datetime import datetime, date
from api.models import User, Product, Payment, Deal
import requests

from api.utils import (
    create_payments,
    create_deals
)

BRANCHES = settings.BRANCHES_ID
TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
CHAT_ID = settings.CHAT_ID

def send_message(message):
    api_url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'protect_content': True,
    }

    response = requests.post(api_url, json=payload)

def error_handler(message):
    today = date.today()

    users = User.objects.filter(created_at__date=today).count()
    payments = Payment.objects.filter(created_at__date=today).count()
    deals = Deal.objects.filter(created_at__date=today).count()
    products = Product.objects.filter(created_at__date=today).count()

    main = f'Технический отчет 📊\n\n' \
        + f'📅 Дата: {today}\n' \
        + f'👤 Создано пользователей: {users} шт\n' \
        + f'💳 Созданные платежи: {payments} шт\n' \
        + f'🛍 Созданные сделки: {deals} шт\n' \
        + f'📦Созданные товары: {products} шт\n\n' \
        + f'Статус:\n{message} ❌'

    send_message(main)

def success_handler(status):
    today = date.today()

    users = User.objects.filter(created_at__date=today)
    payments = Payment.objects.filter(created_at__date=today)
    deals = Deal.objects.filter(created_at__date=today)
    products = Product.objects.filter(created_at__date=today)

    message = f'Технический отчет 📊\n\n' \
        + f'📅  Дата: {today}\n' \
        + f'👤  Созданные пользователи: {users.count()} шт\n' \
        + f'💳  Созданные платежи: {payments.count()} шт\n' \
        + f'🛍  Созданные сделки: {deals.count()} шт\n' \
        + f'📦  Созданные товары: {products.count()} шт\n\n' \
        + f'Статус:\n{status} ✅'

    send_message(message)

    uzs_payments = payments.filter(payment_type__currency__name='Base Sum').aggregate(total_amount=Sum('amount'))['total_amount']
    if not uzs_payments:
        uzs_payments = 0
    uzs_payments = round(uzs_payments, 2)

    usd_payments = payments.filter(payment_type__currency__name='USD').aggregate(total_amount=Sum('amount'))['total_amount']
    if not usd_payments:
        usd_payments = 0
    usd_payments = round(usd_payments, 2)

    uzs_deals = deals.filter(payment_type__currency__name='SUM').aggregate(total_amount=Sum('total'))['total_amount']
    if not uzs_deals:
        uzs_deals = 0
    uzs_deals = round(uzs_deals, 2)

    usd_deals = deals.filter(payment_type__currency__name='USD').aggregate(total_amount=Sum('total'))['total_amount']
    if not usd_deals:
        usd_deals = 0
    usd_deals = round(usd_deals, 2)

    message = f'Финансовый отчет 📊\n\n' \
        + f'📅  Дата: {today}\n\n' \
        + f'💸  Валюта: USD\n' \
        + f'💵  Сумма платежей: {usd_payments}\n' \
        + f'🛍  Сумма сделок: {usd_deals}\n\n' \
        + f'💶  Валюта: UZS\n' \
        + f'💳  Сумма платежей: {uzs_payments}\n' \
        + f'🛍  Сумма сделок: {uzs_deals}\n\n' \
        + f'Статус:\n{status} ✅'
    send_message(message)

class Command(BaseCommand):
    help = 'Send message to customers who has payment for today'

    def handle(self, *args, **options):
        date = datetime.now().strftime('%d.%m.%Y')

        for branch in BRANCHES:

            if not create_payments(branch, date):
                error_handler("Ошибка при создании платежей")
                return

            if not create_deals(branch, date):
                error_handler("Ошибка при создании сделок")
                return

        success_handler('Данные перенесены успешно')