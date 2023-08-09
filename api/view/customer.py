import requests
import xmltodict

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import XMLParser

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from api.models import User, District, Branch
from api.serializer.customer import UserSerializer

LOGIN = settings.SMARTUP_LOGIN
PASSWORD = settings.SMARTUP_PASSWORD        
API_BASE = settings.SMARTUP_URL

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateUserView(APIView):

    def post(self, request):
        if 'branch' not in request.POST:
            return Response(status=400)
        
        if not Branch.objects.filter(smartup_id=request.POST['branch']).exists():
            return Response(status=404)
        
        branch = Branch.objects.get(smartup_id=request.POST['branch'])
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

        if response.status_code == 200:
            parser = XMLParser()
            parser.feed(response.text.encode('utf-8'))  # Encode the XML data as bytes
            element = parser.close()  # Get the parsed element

            # Convert the parsed element back to XML text
            cleaned_xml = ET.tostring(element, encoding='unicode')

            for text in element.itertext():
                print(text)
            
            return Response(data=cleaned_xml, status=200)
            
        return Response(status=500)
    