import requests

from django.conf import settings
from lxml import etree

from api.models import User, District
from .get_data import get_data
from .phone import validate_phone_number, format_phone_number

LOGIN = settings.SMARTUP_LOGIN
PASSWORD = settings.SMARTUP_PASSWORD        
API_BASE = settings.SMARTUP_URL

def create_customers(branch):
    url = f'https://{API_BASE}/b/es/porting+exp$legal_person'
        
    xml_data = f"""
        <?xml version="1.0" encoding="utf-8"?>
        <Root>
            <Logon>
                <login>{LOGIN}</login>
                <password>{PASSWORD}</password>
                <filial>{branch}</filial>
            </Logon>
        </Root>
        """
    xml_data = xml_data.strip()
    
    headers = {
        'Content-Type': 'application/xml',
    }
    
    response = requests.post(url, data=xml_data, headers=headers)
    if response.status_code != 200:
        return None
    
    try:
        parser = etree.XMLParser(recover=True)
        root = etree.fromstring(response.content, parser=parser)

        customers = root.xpath("//Контрагент")
        
        customer_data = []
        for customer in customers:
            name = customer.find("ПолноеНазваниеКонтрагента").text
            try:
                phone = customer.find("КонтактыКонтрагент/ОсновнойТелефон").text
            except:
                phone = None
            customer_id = customer.find("ИдКонтрагент").text
            district = customer.find("Район").text
            address = customer.find("ОсновнойАдрес").text
            
            customer_info = {
                "name": name,
                "phone": phone,
                "id": customer_id,
                "district": district,
                "address": address,
            }
            customer_data.append(customer_info)
            
        for customer in customer_data:
            if not User.objects.filter(smartup_id=customer['id']).exists():
                phone = customer['phone']
                if phone and not validate_phone_number(phone):
                    phone = format_phone_number(phone)
                user = User.objects.create(
                    smartup_id=customer['id'],
                    name=customer['name'],
                    phone=phone,
                    address=customer['address']
                )
                if customer['district'] and District.objects.filter(name=customer['district']):
                    district = District.objects.filter(name=customer['district']).first()
                    user.district = district
                    user.save()
        return True
    except:
        return None

def create_customer(id: str):
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
   
    data = get_data('/b/ref/legal_person/legal_person_list&table', columns=columns, filter=filter)
    
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