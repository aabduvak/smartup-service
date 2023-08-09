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
    def get(self, request):
        if 'Sessionid' not in request.headers:
            return Response(status=401)
        
        columns = [
            "region_id",
            "name",
            "lat_lng"
        ]
        session = request.headers['Sessionid']
        
        response = get_data(endpoint='/b/anor/mr/region_list+x&table', session=session, columns=columns)
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
        return_data = [{"id": region.id, "smartup_id": region.smartup_id, "name": region.name, 'created_at': region.created_at} for region in regions]
        
        return Response(return_data, status=200)

class CreateCitiesView(APIView):
    def get(self, request):
        if 'Sessionid' not in request.headers:
            return Response(status=400)
        
        session = request.headers['Sessionid']
        
        regions = Region.objects.all()
        
        for region in regions:
            columns = [
                "region_id",
                "name",
                "lat_lng"
            ]
            
            response = get_data(endpoint='/b/anor/mr/region_list+cities&table', session=session, columns=columns, parent=region.smartup_id)
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
        return_data = [{"id": city.id, "smartup_id": city.smartup_id, "name": city.name, 'region': city.region.name, 'created_at': city.created_at} for city in cities]
        
        return Response(return_data, status=200)

class CreateDistrictsView(APIView):
    def get(self, request):
        if 'Sessionid' not in request.headers:
            return Response(status=400)
        
        session = request.headers['Sessionid']
        
        cities = City.objects.all()
        
        for city in cities:
            columns = [
                "region_id",
                "name",
                "lat_lng"
            ]
            
            response = get_data(endpoint='/b/anor/mr/region_list+towns&table', session=session, columns=columns, parent=city.smartup_id)
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
        return_data = [{"id": town.id, "smartup_id": town.smartup_id, "name": town.name, 'region': town.city.name, 'created_at': town.created_at} for town in towns]
        
        return Response(return_data, status=200)