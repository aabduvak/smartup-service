from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import date

from api.utils import (
    get_payment_list,
    get_debt_list,
    disabled_workplace,
    send_telegram_message,
)
from api.models import *
from api.utils.eskiz import get_token, get_balance, send_message, get_nickname

BRANCHES_ID = settings.BRANCHES_ID
STATUS_LIST = ["DELIVRD", "TRANSMTD", "WAITING"]


def success_handler(status, data, token):
    today = date.today()
    balance = get_balance(token)["data"]["balance"]

    message = (
        f"Отчет от провайдера Eskiz.uz 📊\n\n"
        + f"📅  Дата: {today}\n\n"
        + f'Отправленные сообщения: {data["success"]} шт\n'
        + f'Неверные номера: {data["invalid"]} шт\n'
        + f'Отключенные клиенты: {data["disabled"]} шт\n'
        + f'Неотправленные сообщения: {data["error"]} шт\n'
        + f"Текущий баланс: {balance} сум\n\n"
        + f"Статус:\n{status} ✅"
    )

    send_telegram_message(message)


def prepare_message(customer, payment, debt):
    currency_name = payment.payment_type.currency.name
    if currency_name.lower() == "base sum" or currency_name.lower() == "sum":
        currency_name = "UZS"

    payment_date = payment.date_of_payment.strftime("%d/%m/%Y")

    message = f"Hurmatli {customer.name}\nOOO GLAMOUR COSMETICS korxonasiga {payment_date} kuni amalga oshirgan {payment.amount} {currency_name} miqdoridagi to'lovingiz qabul qilindi. "

    if debt:
        if len(debt["customers"]) == 1:
            message += f'Mavjud balans {debt["customers"][0]["amount"]} {debt["customers"][0]["currency"]}'
        elif len(debt["customers"]) == 2:
            message += f'Mavjud balans {debt["customers"][0]["amount"]} {debt["customers"][0]["currency"]} va {debt["customers"][1]["amount"]} {debt["customers"][1]["currency"]}'

    return message


def send_messages():
    token = get_token()
    if token is None:
        return  # Invalid token

    token = token["data"]["token"]
    nick = get_nickname(token)

    data = {"success": 0, "error": 0, "invalid": 0, "disabled": 0}

    for branch in BRANCHES_ID:
        payments = get_payment_list(branch)
        for payment in payments:
            customer = payment.customer

            if disabled_workplace(customer):
                data["disabled"] += 1
                continue

            if not customer.phone:
                data["invalid"] += 1
                continue

            debt = get_debt_list(branch_id=branch, customer_id=customer.smartup_id)
            message = prepare_message(customer, payment, debt)

            # state = send_message(customer.phone[1:], message, token, nick)
            # if state and state["status"].upper() in STATUS_LIST:
            #    data["success"] += 1
            # else:
            #    data["error"] += 1

    success_handler("Отправлено сообщение клиентам, у которых есть оплата", data, token)


class Command(BaseCommand):
    help = "Send message to customers who has payment for today"

    def handle(self, *args, **options):
        send_messages()
