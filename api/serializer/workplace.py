from rest_framework.serializers import ModelSerializer
from api.models import User, WorkPlace


class WorkPlaceSerializer(ModelSerializer):
    class Meta:
        model = WorkPlace
        fields = ("id", "code", "smartup_id", "name")
