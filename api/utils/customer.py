import requests
from django.urls import reverse
from django.conf import settings

from .get_data import get_data
from .get_token import obtain_token

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
   
    customer = get_data('/b/ref/legal_person/legal_person_list&table', columns=columns, session=session, filter=filter)
    return customer