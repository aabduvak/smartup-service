import requests

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token

from django.conf import settings

LOGIN = settings.SMARTUP_LOGIN
PASSWORD = settings.SMARTUP_PASSWORD        
API_BASE = settings.SMARTUP_URL

class AuthView(APIView):
    def get(self, request):
        return Response(status=200)
    
    def post(self, request):
        url = f'https://{API_BASE}/b/anor/s$logon'
        
        data = {
            'login': LOGIN,
            'password': PASSWORD
        }
        response = requests.post(url, data)
        
        if response.status_code == 200:
            return Response(response.cookies.get_dict())
        return Response(status=response.status_code)

class CustomerListView(APIView):
    
    def get(self, request):
        
        if 'Sessionid' not in request.headers:
            return Response(status=400)

        session = request.headers['Sessionid']        
        
        url = f'https://{API_BASE}/b/ref/legal_person/legal_person_list&table'
        
        header = {
            'Cookie': session,
        }
        
        data = {
            "p": {
                "column": [
                    "person_id",
                    "code",
                    "name",
                    "main_phone",
                    "region_name"

                ],
                "filter": [],
                "sort": [],
                "offset": 0,
                "limit": 50
            },
            "d": {
                "is_filial": "N"
            }
        }
        
        response = requests.post(url, json=data, headers=header)
        if response.status_code == 200:
            return Response(response.json())
        return Response(response.status_code)
