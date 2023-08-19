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
    create_deals
)

BRANCHES = settings.BRANCHES_ID

def error_handler(message, date):
    print(message)

def success_handler(message, date):
    print(message)

class Command(BaseCommand):
    help = 'Send message to customers who has payment for today'

    def handle(self, *args, **options):
        date = datetime.now().strftime('%d.%m.%Y')
        
        if not create_currency():
            error_handler("Error while creating currency", date)
        
        if not create_payment_type():
            error_handler("Error while creating payment type", date)
        
        if not create_places():
            error_handler("Error while creating places", date)
            
        for branch in BRANCHES:
            if not create_products(branch):
                error_handler("Error while creating products", date)
            
            if not create_customers(branch):
                error_handler("Error while creating customers", date)
            
            if not create_payments(branch):
                error_handler("Error while creating payments", date)
            
            if not create_deals(branch, date):
                error_handler("Error while creating deals", date)
        
        success_handler("All data migrated successfully", date)