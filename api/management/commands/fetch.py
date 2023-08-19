from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime


from api.utils import (
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
            
        for branch in BRANCHES:
            
            if not create_payments(branch):
                error_handler("Error while creating payments", date)
            
            if not create_deals(branch, date):
                error_handler("Error while creating deals", date)
        
        success_handler("All data migrated successfully", date)