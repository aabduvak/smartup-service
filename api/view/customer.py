import requests

from lxml import etree
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from api.models import User, Branch, District
from api.serializer.customer import UserSerializer
from api.utils.phone import validate_phone_number, format_phone_number

LOGIN = settings.SMARTUP_LOGIN
PASSWORD = settings.SMARTUP_PASSWORD        
API_BASE = settings.SMARTUP_URL

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(APIView):
    def get(self, request, smartup_id):
        if smartup_id is None:
            return Response(status=400)
        
        if not User.objects.filter(smartup_id=smartup_id):
            return Response(status=404)
        
        user = User.objects.get(smartup_id=smartup_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
            

class CreateUserView(APIView):    
    def post(self, request):
        print(request.data)
        if not 'branch' in request.data:
            return Response(status=400)
        
        if not Branch.objects.filter(smartup_id=request.data['branch']).exists():
            return Response(status=404)
        
        branch = Branch.objects.get(smartup_id=request.data['branch'])
        url = f'https://{API_BASE}/b/es/porting+exp$legal_person'
        
        xml_data = f"""
            <?xml version="1.0" encoding="utf-8"?>
            <Root>
                <Logon>
                    <login>{LOGIN}</login>
                    <password>{PASSWORD}</password>
                    <filial>{branch.smartup_id}</filial>
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

            customers = root.xpath("//Контрагент")
            
            customer_data = []
            for customer in customers:
                name = customer.find("ПолноеНазваниеКонтрагента").text
                phone = customer.find("КонтактыКонтрагент/ОсновнойТелефон").text
                customer_id = customer.find("ИдКонтрагент").text
                district = customer.find("Район").text

                customer_info = {
                    "name": name,
                    "phone": phone,
                    "id": customer_id,
                    "district": district
                }
                customer_data.append(customer_info)
                
            for customer in customer_data:
                if not User.objects.filter(smartup_id=customer['id']).exists():
                    
                    phone = customer['phone']
                    if not validate_phone_number(phone):
                        phone = format_phone_number(phone)
                    user = User.objects.create(
                        smartup_id=customer['id'],
                        name=customer['name'],
                        phone=phone,  
                    )
                    if customer['district'] and District.objects.filter(name=customer['district']):
                        district = District.objects.filter(name=customer['district']).first()
                        user.district = district
                        user.save()
            
            users = User.objects.all()
            user_serializer = UserSerializer(users, many=True)
            return Response(data=user_serializer.data)
        except:
            return Response(status=400)
