import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Region, City, District

LOGIN = settings.SMARTUP_LOGIN
PASSWORD = settings.SMARTUP_PASSWORD        
API_BASE = settings.SMARTUP_URL

class AuthView(APIView):
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
