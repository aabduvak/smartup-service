from datetime import datetime, date
from django.db.models import Q
from api.models import User, Payment

def get_payment_list(branch_id):
    today = date.today()

    payments_query = Payment.objects.filter(
        Q(date_of_payment=today) & Q(branch__smartup_id=branch_id)
    )
    
    return payments_query
   