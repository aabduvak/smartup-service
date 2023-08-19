from datetime import datetime, date
from django.db.models import Q
from decimal import Decimal
import json
from api.models import User, Payment, Currency
from .get_data import get_data
from .customer import create_customer

def get_payment_list(branch_id, date_of_payment=None):
    payment_date = date.today()
    if date_of_payment:
        payment_date = date_of_payment

    payments_query = Payment.objects.filter(
        Q(date_of_payment=payment_date) & Q(branch__smartup_id=branch_id)
    )
    
    return payments_query

def get_debt_list(branch_id, currency=None, limit=50, customer_id=None):
    columns = [
        "legal_person_id",
        "currency_name",
        "total_amount"
    ]
    filter = []
    if currency == 'USD':
        currency_id = '200'
    elif currency == 'UZS':
        currency_id = '0'
    
    if customer_id and currency:
        filter = [
            "and",
            [
                [
                    "legal_person_id",
                    "=",
                    [
                        customer_id
                    ]    
                ],
                [
                    "currency_id",
                    "=",
                    [
                        currency_id
                    ]
                ]
            ],
        ]
    elif customer_id:
        filter = [
            "legal_person_id",
            "=",
            [
                customer_id
            ] 
        ]
    elif currency:
        filter = [
            "currency_id",
            "=",
            [
                currency_id
            ]
        ]
    
    sort = [
        "total_amount"
    ]
        
    response = get_data(endpoint='/b/cs/payment/payment_list+x&table', limit=limit, columns=columns, sort=sort, filter=filter, branch_id=branch_id)
    if response['count'] <= 0:
        return None
    
    data = {
        "total_company_debt": {
            "USD": 0,
            "UZS": 0
        },
        "total_customer_debt": {
            "USD": 0,
            "UZS": 0
        },
        "total_uzs": 0,
        "total_usd": 0,
        "customers": [],
    }
    
    for customer in response['data']:
        if not User.objects.filter(smartup_id=customer[0]).exists():
            if not create_customer(customer[0]):
                continue
        user = User.objects.get(smartup_id=customer[0])
        currency = Currency.objects.get(name=customer[1])
        
        currency_name = currency.name
        if currency.name.lower() == 'sum' or currency.name.lower() == 'base sum':
            currency_name = "UZS"
            
        item = {
            "smartup_id": customer[0],
            "name": user.name,
            "phone": user.phone,
            "currency": currency_name,
            "amount": float(customer[2]) * -1,
        }
        
        if item["amount"] < 0:
            if item["currency"] == 'USD':
                data["total_company_debt"]['USD'] += item["amount"]
            elif item["currency"] == 'SUM':
                data["total_company_debt"]['UZS'] += item["amount"]
        else:
            if item["currency"] == 'USD':
                data["total_customer_debt"]['USD'] += item["amount"]
            elif item['currency'] == 'SUM':
                data["total_customer_debt"]['UZS'] += item["amount"]

        if user.district:
            item["district"] = user.district.name
            item["city"] = user.district.city.name
        data["customers"].append(item)

    data["total_usd"] = data["total_company_debt"]['USD'] + data["total_customer_debt"]["USD"]
    data["total_uzs"] = data["total_company_debt"]['UZS'] + data["total_customer_debt"]["UZS"]
    return data