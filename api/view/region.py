from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date

from api.serializer.region import RegionSerializer, CitySerializer, DistrictSerializer
from api.models import Region, City, District
from api.utils.places import create_regions, create_cities, create_districts

class RegionListView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class CityListView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class DistrictListView(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class CreateRegionsView(APIView):
    def post(self, request):
        if not create_regions():
            return Response({'status':'error', 'message': 'error occured while creating regions'}, status=500)
        
        today = date.today()
        
        regions = Region.objects.filter(created_at__date=today)
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data, status=200)

class CreateCitiesView(APIView):
    def post(self, request):
        if not create_cities():
            return Response({'status':'error', 'message': 'error occured while creating cities'}, status=500)
        
        today = date.today()

        cities = City.objects.filter(created_at__date=today)
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=200)

class CreateDistrictsView(APIView):
    def post(self, request):
        if not create_districts():
            return Response({'status':'error', 'message': 'error occured while creating districts'}, status=500)

        today = date.today()

        towns = District.objects.filter(created_at__date=today)
        serializer = DistrictSerializer(towns, many=True)
        return Response(serializer.data, status=200)