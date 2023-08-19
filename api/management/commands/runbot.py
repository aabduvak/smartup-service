from django.core.management.base import BaseCommand
from django.conf import settings
from api.bot.bot import main

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN

class Command(BaseCommand):
    help = 'Send message to customers who has payment for today'

    def handle(self, *args, **options):
        main()