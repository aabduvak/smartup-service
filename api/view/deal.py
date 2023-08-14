import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.conf import settings
from lxml import etree
from datetime import datetime
from decimal import Decimal

from api.models import User, Deal, Branch, PaymentType
from api.serializer.deal import DealSerializer
from api.utils.payment_type import create_payment_type
from api.utils.customer import create_customer

API_BASE = settings.SMARTUP_URL
LOGIN = settings.SMARTUP_LOGIN
PASSWORD = settings.SMARTUP_PASSWORD

class DealListView(ListAPIView):
    serializer_class = DealSerializer
    queryset = Deal.objects.all()

class DealDetailView(APIView):
    def get(self, request, smartup_id):
        if not smartup_id:
            return Response(status=400)
        
        if not Deal.objects.filter(smartup_id=smartup_id).exists():
            pass
        
        return Response(status=200)

class CreateDealView(APIView):
    def post(self, request):
        if not 'branch' in request.data:
            return Response(status=400)
        
        if not Branch.objects.filter(smartup_id=request.data['branch']).exists():
            return Response(status=404)
        
        date = datetime.now().strftime('%d.%m.%Y')
        if 'date' in request.data:
            date = request.data['date']
            
        branch = Branch.objects.get(smartup_id=request.data['branch'])
        url = f'https://{API_BASE}/b/es/porting+exp$deal'
        
        xml_data = f"""
            <?xml version="1.0" encoding="utf-8"?>
            <Root>
                <Logon>
                    <login>{LOGIN}</login>
                    <password>{PASSWORD}</password>
                    <filial>{branch.smartup_id}</filial>
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
            return Response(status=response.status_code)
        
        try:
            parser = etree.XMLParser(recover=True)
            root = etree.fromstring(response.content, parser=parser)

            deals = root.xpath("//Сделка")
            
            for deal in deals:
                info = {
                    "deal_id": deal.find("СделкаИд").text,
                    "customer_id": deal.find("КонтрагентИд").text,
                    "payment_type_id": deal.find("ТипОплатыИд").text,
                    "amount": deal.find("Оплата/Сумма").text,
                    "date_of_order": deal.find("ДатаСделки").text,
                    "date_of_shipment": deal.find("ДатаОтгрузки").text,
                    "products": {}
                }

                if not PaymentType.objects.filter(smartup_id=info['payment_type_id']).exists():
                    create_payment_type()
                
                if not User.objects.filter(smartup_id=info['customer_id']).exists():
                    create_customer(info['customer_id'])
                
                user = User.objects.get(smartup_id=info['customer_id'])
                payment_type = PaymentType.objects.get(smartup_id=info['payment_type_id'])
                amount =  Decimal(info['amount'])
                date_of_shipment = datetime.strptime(info['date_of_shipment'], '%d.%m.%Y').date()
                date_of_order = datetime.strptime(info['date_of_order'], '%d.%m.%Y').date()
                
                deal = Deal.objects.create(
                    smartup_id=info['deal_id'],
                    customer=user,
                    payment_type=payment_type,
                    date_of_order=date_of_order,
                    date_of_payment=date_of_shipment,
                    total=amount,
                )
            
            payments = Payment.objects.all()
            serializer = PaymentSerializer(payments, many=True) 
            return Response(data=serializer.data)
        except:
            return Response(status=500)