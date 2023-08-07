from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.models import Region, City, District
from api.serializer.region import RegionSerializer, CitySerializer, DistrictSerializer

class RegionListView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class CityListView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class DistrictListView(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
