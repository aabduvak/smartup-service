import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime, date

from api.utils.payment import get_payment_list, get_debt_list
from api.models import *

ESKIZ_EMAIL = settings.ESKIZ_EMAIL
ESKIZ_PASSWORD = settings.ESKIZ_PASSWORD
ESKIZ_URL = settings.ESKIZ_URL
BRANCHES_ID = settings.BRANCHES_ID

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
CHAT_ID = settings.CHAT_ID

def send_telegram_message(message):
    api_url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'protect_content': True,
    }

    response = requests.post(api_url, json=payload)

def success_handler(status, data):
    today = date.today()

    message = f'Отчет от провайдера 📊\n\n' \
        + f'📅  Дата: {today}\n' \
        + f'📤  Отправленные сообщения: {data["success"]} шт\n' \
        + f'📥  Неотправленные сообщения: {data["error"]} шт\n\n' \
        + f'Статус:\n{status} ✅'
    
    send_telegram_message(message)

def get_token():
    url = f'http://{ESKIZ_URL}/auth/login'
    data = {
        "email": ESKIZ_EMAIL,
        "password": ESKIZ_PASSWORD
    }
    
    response = requests.post(url=url, data=data)
    if response.status_code == 200:
        return response.json()
    return None

def delete_token(token):
    url = f'http://{ESKIZ_URL}/auth/invalidate'
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(url=url, headers=headers)
    return response
    

def send_message(phone, message, token):
    url = f'http://{ESKIZ_URL}/message/sms/send'
    
    data = {
        "mobile_phone": phone,
        "message": message,
        "from": "4546",
    }
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(url=url, data=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

def prepare_message(customer, payment, debt):
    currency_name = payment.payment_type.currency.name
    if currency_name.lower() == 'base sum' or currency_name.lower() == 'sum':
        currency_name = 'UZS'
                
    payment_date = payment.date_of_payment.strftime("%d/%m/%Y")
    
    message = f'Hurmatli {customer.name}\nOOO GLAMOUR COSMETICS korxonasiga {payment_date} kuni amalga oshirgan {payment.amount} {currency_name} miqdoridagi to\'lovingiz qabul qilindi. '
            
    if debt:
        if len(debt['customers']) == 1:
            message += f'Mavjud balans {debt["customers"][0]["amount"]} {debt["customers"][0]["currency"]}'
        elif len(debt['customers']) == 2:
            message += f'Mavjud balans {debt["customers"][0]["amount"]} {debt["customers"][0]["currency"]} va {debt["customers"][1]["amount"]} {debt["customers"][1]["currency"]}'
    
    return message

def send_messages():
    token = get_token()
    if token is None:
        return # Invalid token
    
    token = token['data']['token']
    data = {
        'success': 3,
        'error': 0
    }
    

    for branch in BRANCHES_ID:
        payments = get_payment_list(branch, date_of_payment='2023-08-18')
        
        for payment in payments:
            if not payment.customer.phone:
                continue
            

            customer = payment.customer
            debt = get_debt_list(branch_id=branch, customer_id=customer.smartup_id)
            message = prepare_message(customer, payment, debt)

            state = send_message(customer.phone[1:], message, token)
            if not state or state['status'] not in ['Waiting', 'DELIVRD', 'TRANSMTD']:
                data['error'] += 1
            else:
                data['success'] += 1
    
    success_handler('Отправлено сообщение клиентам, у которых есть оплата', data=data)


class Command(BaseCommand):
    help = 'Send message to customers who has payment for today'

    def handle(self, *args, **options):
        send_messages()