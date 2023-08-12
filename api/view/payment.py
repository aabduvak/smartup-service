import requests

from datetime import datetime
from lxml import etree
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.conf import settings
from decimal import Decimal
from datetime import datetime

from api.serializer.payment import PaymentSerializer
from api.models import Payment, Branch, User, PaymentType
from api.utils.customer import create_customer

LOGIN = settings.SMARTUP_LOGIN
PASSWORD = settings.SMARTUP_PASSWORD        
API_BASE = settings.SMARTUP_URL

class PaymentListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        queryset = Payment.objects.all()
        
        user_id = self.request.query_params.get('customer')
        branch = self.request.query_params.get('branch')
        date = self.request.query_params.get('date')
        currency = self.request.query_params.get('currency')
        payment_type = self.request.query_params.get('payment_type')
                
        if user_id and User.objects.filter(smartup_id=user_id).exists():
            queryset = queryset.filter(customer__smartup_id=user_id)
        
        if branch and Branch.objects.filter(smartup_id=branch).exists():
            queryset = queryset.filter(branch__smartup_id=branch)
        
        if date:
            date_of_payment = datetime.strptime(date, '%d.%m.%Y')
            queryset = queryset.filter(date_of_payment=date_of_payment.strftime('%Y-%m-%d'))
        
        if currency:
            queryset = queryset.filter(payment_type__currency__name=currency)
        
        if payment_type:
            queryset = queryset.filter(payment_type__smartup_id=payment_type)
        
        return queryset

class PaymentDetailView(APIView):
    def get(self, request, smartup_id):
        if not smartup_id:
            return Response({'error':'smartup_id is required'}, status=400)
        
        if not Payment.objects.filter(smartup_id=smartup_id).exists():
            return Response({'error':'payment not found'}, status=404)
        
        payment = Payment.objects.get(smartup_id=smartup_id)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

class CreatePaymentView(APIView):
    def post(self, request):
        if not 'branch' in request.data:
            return Response(status=400)
        
        if not Branch.objects.filter(smartup_id=request.data['branch']).exists():
            return Response(status=404)
        
        date = datetime.now().strftime('%d.%m.%Y')
        if 'date' in request.data:
            date = request.data['date']
            
        branch = Branch.objects.get(smartup_id=request.data['branch'])
        url = f'https://{API_BASE}/b/es/porting+exp$payment'
        
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

            payments = root.xpath("//Оплата")
            
            for payment in payments:
                info = {
                    "customer_id": payment.find("ИдКонтрагента").text,
                    "payment_id": payment.find("ИдОплаты").text,
                    "payment_type_id": payment.find("ИдТипаОплаты").text,
                    "amount": payment.find("Сумма").text,
                    "base_amount": payment.find("Базовая").text,
                    "date_of_payment": payment.find("ДатаОплаты").text,
                }

                if Payment.objects.filter(smartup_id=info['payment_id']).exists():
                    continue
                
                if not User.objects.filter(smartup_id=info['customer_id']).exists():
                    create_customer(info['customer_id'])
                
                user = User.objects.get(smartup_id=info['customer_id'])
                payment_type = PaymentType.objects.get(smartup_id=info['payment_type_id'])
                amount =  Decimal(info['amount'])
                base_amount = Decimal(info['base_amount'])
                date_of_payment = datetime.strptime(info['date_of_payment'], '%d.%m.%Y').date()
                
                payment = Payment.objects.create(
                    smartup_id=info['payment_id'],
                    customer=user,
                    payment_type=payment_type,
                    amount=amount,
                    base_amount=base_amount,
                    date_of_payment=date_of_payment.strftime('%Y-%m-%d'),
                    branch=branch,
                )
            
            payments = Payment.objects.all()
            serializer = PaymentSerializer(payments, many=True) 
            return Response(data=serializer.data)
        except:
            return Response(status=500)