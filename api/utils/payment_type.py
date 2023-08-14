from api.models import PaymentType, Currency

from .get_data import get_data
from .get_token import obtain_token

def create_payment_type():
    session = obtain_token()

    columns = [
        "payment_type_id",
        "name",
        "currency_name"
    ]
    
    response = get_data(endpoint='/b/anor/mkr/payment_type_list+x&table', session=session, columns=columns, remove_parent=True, filter=filter)
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