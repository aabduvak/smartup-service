import requests
from django.core.management.base import BaseCommand
from django.conf import settings

from api.utils.payment import get_payment_list

ESKIZ_EMAIL = settings.ESKIZ_EMAIL
ESKIZ_PASSWORD = settings.ESKIZ_PASSWORD
ESKIZ_URL = settings.ESKIZ_URL
BRANCHES_ID = settings.BRANCHES_ID

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
    print(response.text)
    return None
    

def send_messages():
    data = get_token()
    if data is None:
        return # Invalid token
    
    token = data['data']['token']
    
    for branch in BRANCHES_ID:
        payments = get_payment_list(branch)
        
        for payment in payments:
            if not payment.customer.phone:
                continue
            currency_name = payment.payment_type.currency.name
            
            if currency_name.lower() == 'base sum':
                currency_name = 'UZS'

            message = f'Hurmatli {payment.customer.name}\nOOO GLAMOUR COSMETICS korxonasiga amalga oshirgan {payment.amount} {currency_name} miqdoridagi to\'lovingiz qabul qilindi. '
            customer = payment.customer
            
            state = send_message(customer.phone[1:], message, token)
            print(state)
            return state       

class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        send_messages()