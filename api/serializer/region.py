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
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['region'] and instance.region:
            representation['region'] = instance.region.name
        return representation

class DistrictSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['city'] and instance.city:
            representation['city'] = instance.city.name
        return representation
