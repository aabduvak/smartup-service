from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.conf import settings
from datetime import date

from api.models import WorkPlace
from api.serializer.workplace import WorkPlaceSerializer
from api.serializer.customer import UserSerializer
from api.utils.workplace import create_workplaces, create_workplace

BRANCHES = settings.BRANCHES_ID

class WorkPlaceListView(ListAPIView):
    queryset = WorkPlace.objects.all()
    serializer_class = WorkPlaceSerializer


class WorkPlaceDetailView(APIView):
    def get(self, request, smartup_id):
        if not smartup_id:
            return Response(status=400)
        
        if not WorkPlace.objects.filter(smartup_id=smartup_id).exists():
            for branch in BRANCHES:
                if create_workplace(id=smartup_id, branch_id=branch):
                    break

        if not WorkPlace.objects.filter(smartup_id=smartup_id).exists():
            return Response(status=404)
        
        workplace = WorkPlace.objects.get(smartup_id=smartup_id)
        customers = workplace.customers.all()
        
        serializer = WorkPlaceSerializer(workplace)
        user_serializer = UserSerializer(customers, many=True)
        
        data = serializer.data
        users = user_serializer.data

        data['customers'] = users
        return Response(data)


class CreateWorkPlaceView(APIView):
    permission_classes = [IsAdminUser,]
    
    def post(self, request):
        for branch in BRANCHES:
            if not create_workplaces(branch):
                return Response({'status':'error', 'message': 'error occured while creating workplaces'}, status=500)
        
        today = date.today()

        workplaces = WorkPlace.objects.filter(created_at__date=today)
        serializer = WorkPlaceSerializer(workplaces, many=True)
        return Response(serializer.data, status=200)