from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime

from api.utils.payment import create_payments
from api.utils.payment_type import create_payment_type
from api.utils.deal import create_deals

BRANCHES = settings.BRANCHES_ID

class Command(BaseCommand):
    help = 'Send message to customers who has payment for today'

    def handle(self, *args, **options):
        date = datetime.now().strftime('%d.%m.%Y')
        create_payment_type()
        for branch in BRANCHES:
            create_payments(branch, date)
            create_deals(branch, date)
            
            
