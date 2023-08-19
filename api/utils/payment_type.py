from api.models import PaymentType, Currency

from .get_data import get_data

def create_currency():
    columns = [
        "name",
        "state_name",
        "currency_id"
    ]
    
    response = get_data(endpoint='/b/anor/mk/currency_list+x&table', columns=columns)
    if  response['count'] <= 0:
        return None
    currencies = response['data']
    
    try:    
        for currency in currencies:
            if not Currency.objects.filter(name=currency[0]).exists():
                Currency.objects.create(
                    name=currency[0]
                )
        return True
    except:
        return None

def create_payment_type():

    columns = [
        "payment_type_id",
        "name",
        "currency_name"
    ]
    
    response = get_data(endpoint='/b/anor/mkr/payment_type_list+x&table', columns=columns, remove_parent=True)
    if response['count'] <= 0:
        return None
    
    payment_types = response['data']
    
    try:
        for payment_type in payment_types:
            if not PaymentType.objects.filter(smartup_id=payment_type[0]).exists():
                currency = Currency.objects.get(name=payment_type[2])
                
                return PaymentType.objects.create(
                    smartup_id=payment_type[0],
                    name=payment_type[1],
                    currency=currency
                )
        return True
    except:
        return None