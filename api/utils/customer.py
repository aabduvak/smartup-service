import requests

from django.conf import settings
from lxml import etree

from api.models import User, District, WorkPlace
from .get_data import get_data
from .phone import validate_phone_number, format_phone_number
from .workplace import create_workplace

LOGIN = settings.SMARTUP_LOGIN
PASSWORD = settings.SMARTUP_PASSWORD        
API_BASE = settings.SMARTUP_URL

def get_customer_from_service(id, branch_id=None):
    columns = [
        "person_id",
        "name",
        "main_phone",
        "region_name",
        "post_address",
        "ref_code",
        "state",
        "room_names",
        "in_filial_state"
    ]
    
    filter = [
        "person_id",
        "=",
        id
    ]
   
    data = get_data('/b/ref/legal_person/legal_person_list&table', columns=columns, filter=filter, branch_id=branch_id)
    
    if data['count'] <= 0:
        return None
    
    customer = data['data'][0]
    return customer

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
    
    parser = etree.XMLParser(recover=True)
    root = etree.fromstring(response.content, parser=parser)

    customers = root.xpath("//Контрагент")
    
    customer_data = []
    for customer in customers:
        customer_id = customer.find("ИдКонтрагент").text
        name = customer.find("ПолноеНазваниеКонтрагента").text
        
        if User.objects.filter(smartup_id=customer_id).exists():
            continue
        district = customer.find("Район").text
        address = customer.find("ОсновнойАдрес").text
        
        try:
            phone = customer.find("КонтактыКонтрагент/ОсновнойТелефон").text
        except:
            phone = None
        
        customer_info = {
            "name": name,
            "phone": phone,
            "id": customer_id,
            "district": district,
            "address": address,
            "workplaces": []
        }
        
        parent = customer.find('РабочиеМестоКонтрагента')
        if parent:
            workplaces = parent.findall("РабочееМесто")
            for workplace in workplaces:
                customer_info["workplaces"].append({
                    'id': workplace.find('ИдРабочегеМесто').text,
                    'code': workplace.find('КодРабочегеМесто').text,
                    'name': workplace.find('НазваниеРабочегеМесто').text
                })                

        if customer_info["phone"] and not validate_phone_number(customer_info["phone"]):
            customer_info["phone"] = format_phone_number(customer_info["phone"])

        user = User.objects.create(
            smartup_id=customer_info['id'],
            name=customer_info['name'],
            phone=customer_info["phone"],
            address=customer_info["address"]
        )
        
        if customer_info['district'] and District.objects.filter(name=customer_info['district']):
            district = District.objects.filter(name=customer_info['district']).first()
            user.district = district
            user.save()
        
        if len(customer_info['workplaces']) > 0:
            for place in customer_info['workplaces']:
                
                if not WorkPlace.objects.filter(smartup_id=place['id']).exists():
                    if not create_workplace(id=place['id'], branch_id=branch):
                        continue
                workplace = WorkPlace.objects.get(smartup_id=place['id'])
                workplace.customers.add(user)
    return True

def create_customer(id: str, branch_id=None):
    customer = get_customer_from_service(id, branch_id)

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
    
    workplace_names = customer[7].split(',')
    for name in workplace_names:
        if WorkPlace.objects.filter(name=name).exists():
            WorkPlace.objects.get(name=name).customers.add(user)
    if District.objects.filter(name=customer[3]).exists():
        user.district = District.objects.filter(name=customer[3]).first()
        user.save()
    return user

columns = [
        "person_id",
        "name",
        "main_phone",
        "region_name",
        "post_address",
        "ref_code",
        "state",
        "room_names",
        "in_filial_state"
    ]

def check_customer_data(id: str, user: User, branch_id=None):
    customer = get_customer_from_service(id, branch_id=branch_id)
    
    if customer[1] != user.name:
        update_customer(id, branch_id)
    if customer[2] != user.phone and validate_phone_number(customer[2]):
        update_customer(id, branch_id)
    if customer[3] != user.district.name:
        update_customer(id, branch_id)
    if customer[4] != user.address:
        update_customer(id, branch_id)
    
    workplace_list = customer[7].split(',')
    for workplace in workplace_list:
        if workplace not in user.workplaces.all():
            update_customer(id, branch_id)
    return True

def update_customer(id: str, branch_id=None):
    customer = get_customer_from_service(id, branch_id)

    if not User.objects.filter(smartup_id=customer[0]).exists():
        return create_customer(id, branch_id)
    
    phone = customer[2]
    if not validate_phone_number(phone):
        phone = format_phone_number(phone)
    
    user = User.objects.get(
        smartup_id=customer[0]
    )
    
    user.name = customer[1]
    user.phone = phone
    user.address = customer[4]
    user.save()
    
    workplaces = user.workplaces.all()
    for workplace in workplaces:
        workplace.customers.remove(user)
    
    workplace_names = customer[7].split(',')
    for name in workplace_names:
        if WorkPlace.objects.filter(name=name).exists():
            WorkPlace.objects.get(name=name).customers.add(user)
    
    if District.objects.filter(name=customer[3]).exists():
        user.district = District.objects.filter(name=customer[3]).first()
        user.save()
    return user