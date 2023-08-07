from rest_framework.serializers import ModelSerializer
from api.models import Region, City, District

class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class DistrictSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'
