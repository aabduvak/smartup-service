from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.conf import settings
from datetime import date

from api.models import User
from api.serializer.customer import UserSerializer
from api.serializer.workplace import WorkPlaceSerializer
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
            for branch in BRANCHES_ID:
                user = create_customer(id=smartup_id, branch_id=branch)
                
                if user:
                    break
            
            if not user:
                return Response(status=404)
        
        user = User.objects.get(smartup_id=smartup_id)
        serializer = UserSerializer(user)
        workplaces_serializer = WorkPlaceSerializer(user.workplaces.all(), many=True)
        
        data = serializer.data
        data['workplaces'] = workplaces_serializer.data
        return Response(data=data)  

class CreateUserView(APIView):
    permission_classes = [IsAdminUser,] 
    def post(self, request):
        branches = BRANCHES_ID
        
        if 'branch' in request.data:
            branches = [request.data['branch']]
            
        for branch in branches:
            if not create_customers(branch):
                return Response({'status':'error', 'message': 'error occured while creating deal'}, status=500)
        
        today = date.today()
        
        users = User.objects.filter(created_at__date=today)
        serializer = UserSerializer(users, many=True)
        return Response({'status':'success', 'result': serializer.data}, status=200)