from datetime import datetime, date
from django.db.models import Q

from api.models import User, Payment
from .get_data import get_data

def get_payment_list(branch_id):
    today = date.today()

    payments_query = Payment.objects.filter(
        Q(date_of_payment=today) & Q(branch__smartup_id=branch_id)
    )
    
    return payments_query

def get_customer_debt_list(branch_id):
    columns = [
        "legal_person_id",
        "legal_person_name",
        "currency_name",
        "total_amount",
        "order_amount",
        "credit_amount",
        "debit_amount",
        "currency_id",
        "full_debit",
        "full_credit",
        "full_order",
        "full_total",
        "all_count"
    ]
    
    # https://banafa.smartup.one
    
    data = get_data(endpoint='/b/cs/payment/payment_list+x&table', columns=columns, branch_id=branch_id)
    if data['count'] <= 0:
        return []
    
    return data['data']