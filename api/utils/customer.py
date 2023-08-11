from api.models import User, District

from .get_data import get_data
from .get_token import obtain_token
from .phone import validate_phone_number, format_phone_number

def create_customer(id: str):
    session = obtain_token()
    
    columns = [
        "person_id",
        "name",
        "main_phone",
        "region_name",
        "post_address",
        "ref_code",
        "state",
        "in_filial_state"
    ]
    
    filter = [
        "person_id",
        "=",
        id
    ]
   
    data = get_data('/b/ref/legal_person/legal_person_list&table', columns=columns, session=session, filter=filter)
    
    if data['count'] <= 0:
        return None
    
    customer = data['data'][0]
    
    if User.objects.filter(smartup_id=customer[0]).exists():
        return User.objects.get(smartup_id=customer[0])
    
    phone = customer[2]
    if not validate_phone_number(phone):
        phone = format_phone_number(phone)
    
    user = User.objects.create(
        smartup_id=customer[0],
        name=customer[1],
        phone=phone,
        address=customer[4]
    )
    
    if District.objects.filter(name=customer[3]).exists():
        user.district = District.objects.filter(name=customer[3]).first()
        user.save()
    return user