from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from datetime import date

from api.models import User
from api.serializer.customer import UserSerializer
from api.utils.customer import create_customer, create_customers

BRANCHES_ID = settings.BRANCHES_ID

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(APIView):
    def get(self, request, smartup_id):
        if smartup_id is None:
            return Response(status=400)
        
        if not User.objects.filter(smartup_id=smartup_id):
            user = create_customer(smartup_id)
            
            if not user:
                return Response(status=404)
        
        user = User.objects.get(smartup_id=smartup_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)            

class CreateUserView(APIView):    
    def post(self, request):
        branches = BRANCHES_ID
        
        if 'branch' in request.data:
            branches = [request.data['branch']]
            
        for branch in branches:
            if not create_customers(branch):
                return Response({'status':'error', 'message': 'error occured while creating deas'}, status=500)
        
        today = date.today()
        
        users = User.objects.filter(created_at__date=today)
        serializer = UserSerializer(users, many=True)
        return Response({'status':'success', 'result': serializer.data}, status=200)