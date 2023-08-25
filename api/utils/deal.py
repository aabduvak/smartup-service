import requests
from django.conf import settings
from lxml import etree
from datetime import datetime
from decimal import Decimal

from api.models import User, Deal, PaymentType, Product, OrderDetails
from .customer import create_customer
from .product import create_product

LOGIN = settings.SMARTUP_LOGIN
PASSWORD = settings.SMARTUP_PASSWORD        
API_BASE = settings.SMARTUP_URL

def create_deal_details(data):
    if not data['deal']:
        return None
    
    product = data['product']
    
    if not Product.objects.filter(code=product['code']).exists():
        create_product(product['code'])
    
    
    prod = Product.objects.get(code=product['code'])
    quantity = int(product['quantity'])
    unit_price = Decimal(product['price'])
    
    data['deal'].total += quantity * unit_price
    data['deal'].save()
    
    detail = OrderDetails.objects.create(
        product=prod,
        deal=data['deal'],
        quantity=quantity,
        unit_price=unit_price,
    )
    
    if data['deal'].payment_type:
        currency = data['deal'].payment_type.currency
        detail.currency = currency
        detail.save()

    return True

def create_deals(branch_id, date):  
    
    url = f'https://{API_BASE}/b/es/porting+exp$deal'
    
    xml_data = f"""
        <?xml version="1.0" encoding="utf-8"?>
        <Root>
            <Logon>
                <login>{LOGIN}</login>
                <password>{PASSWORD}</password>
                <filial>{branch_id}</filial>
                <date>{date}</date>
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

        deals = root.xpath("//Сделка")
        
        for deal in deals:
            info = {
                "deal_id": deal.find("СделкаИд").text,
                "customer_id": deal.find("КонтрагентИд").text,
                "date_of_order": deal.find("ДатаСделки").text,
                "date_of_shipment": deal.find("ДатаОтгрузки").text,
            }
            
            if deal.find(".//ТипОплатыИд") is not None:
                info["payment_type_id"] = deal.find(".//ТипОплатыИд").text
            
            if Deal.objects.filter(smartup_id=info['deal_id']).exists():
                continue

            if not User.objects.filter(smartup_id=info['customer_id']).exists():
                create_customer(info['customer_id'], branch_id=branch_id)
            
            user = User.objects.get(smartup_id=info['customer_id'])
            
            date_of_shipment = datetime.strptime(info['date_of_shipment'], '%d.%m.%Y').date()
            date_of_order = datetime.strptime(info['date_of_order'], '%d.%m.%Y %H:%M:%S').date()
            
            new_deal = Deal.objects.create(
                smartup_id=info['deal_id'],
                customer=user,
                date_of_order=date_of_order,
                date_of_shipment=date_of_shipment,
                total=0,
            )
            
            if 'payment_type_id' in info:
                payment_type = PaymentType.objects.get(smartup_id=info['payment_type_id'])
                new_deal.payment_type = payment_type
                new_deal.save()
            
            product_elements = deal.findall("Строки")
            for product in product_elements:
                data = {
                    "product": {},
                    "deal": new_deal
                }
                
                data['product']['code'] = product.find('НоменклатураКод').text
                data['product']['price'] = product.find('Цена').text
                data['product']['quantity'] = product.find('ПроданоКоличество').text
                data['product']['currency'] = product.find('ВалютаИд').text
                
                if not create_deal_details(data):
                    continue
        return True
    except:
        return None