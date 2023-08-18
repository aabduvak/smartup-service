import requests
from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializer.region import RegionSerializer, CitySerializer, DistrictSerializer
from api.models import Region, City, District
from api.utils.get_data import get_data

LOGIN = settings.SMARTUP_LOGIN
PASSWORD = settings.SMARTUP_PASSWORD        
API_BASE = settings.SMARTUP_URL

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
        columns = [
            "region_id",
            "name",
            "lat_lng"
        ]
        
        response = get_data(endpoint='/b/anor/mr/region_list+x&table', columns=columns)
        if not response:
            return Response(status=500)
        regions = response['data']
        try:    
            for region in regions:
                if not Region.objects.filter(smartup_id=region[0]).exists():
                    Region.objects.create(
                        smartup_id=region[0],
                        name=region[1],
                    )
        except:
            return Response(status=500)
    
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data, status=200)

class CreateCitiesView(APIView):
    def post(self, request):
        regions = Region.objects.all()
        
        for region in regions:
            columns = [
                "region_id",
                "name",
                "lat_lng"
            ]
            
            response = get_data(endpoint='/b/anor/mr/region_list+cities&table', columns=columns, parent=region.smartup_id)
            if not response:
                return Response(status=500)
            cities = response['data']
        
            try:    
                for city in cities:
                    if not City.objects.filter(smartup_id=city[0]).exists():
                        City.objects.create(
                            smartup_id=city[0],
                            name=city[1],
                            region=region
                        )
            except:
                return Response(status=500)
      
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=200)

class CreateDistrictsView(APIView):
    def post(self, request):
        cities = City.objects.all()
        
        for city in cities:
            columns = [
                "region_id",
                "name",
                "lat_lng"
            ]
            
            response = get_data(endpoint='/b/anor/mr/region_list+towns&table', columns=columns, parent=city.smartup_id)
            if not response:
                return Response(status=500)
            towns = response['data']
            
            try:    
                for town in towns:
                    if not District.objects.filter(smartup_id=town[0]).exists():
                        District.objects.create(
                            smartup_id=town[0],
                            name=town[1],
                            city=city
                        )
            except:
                return Response(status=500)
      
        towns = District.objects.all()
        serializer = DistrictSerializer(towns, many=True)
        return Response(serializer.data, status=200)