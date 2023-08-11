import requests

from datetime import datetime
from lxml import etree
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.conf import settings

from api.serializer.payment import PaymentSerializer
from api.models import Payment, Branch

LOGIN = settings.SMARTUP_LOGIN
PASSWORD = settings.SMARTUP_PASSWORD        
API_BASE = settings.SMARTUP_URL

class PaymentListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    # def get_queryset(self):
    #     user_id = self.request.query_params.get('smartup_id')
    #     branch = self.request.query_params.get('branch_id')
    #     date = self.request.query_params.get('date')
        
    #     if user_id:
    #         return Payment.objects.filter(smartup_id=user_id)
    #     elif branch:
    #         return Payment.objects.all()



class PaymentDetailView(APIView):
    def get(self, request, smartup_id):
        if not smartup_id:
            return Response({'error':'smartup_id is required'}, status=400)
        
        if not Payment.objects.filter(smartup_id=smartup_id).exists():
            return Response({'error':'payment not found'}, status=404)
        
        payment = Payment.objects.get(smartup_id=smartup_id)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

class CreatePaymentView(PaymentDetailView):
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
            
            payments_data = []
            for payment in payments:
                customer_id = payment.find("ИдКонтрагента").text
                payment_id = payment.find("ИдОплаты").text
                payment_type_id = payment.find("ИдТипаОплаты").text
                
                # name = payment.find("
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
                        address=address
                    )
                    if customer['district'] and District.objects.filter(name=customer['district']):
                        district = District.objects.filter(name=customer['district']).first()
                        user.district = district
                        user.save()
            
            users = User.objects.all()
            user_serializer = UserSerializer(users, many=True)
            return Response(data=user_serializer.data)
        except:
            return Response(status=500)