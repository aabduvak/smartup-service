from rest_framework.serializers import ModelSerializer

from api.models import Deal

class DealSerializer(ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'