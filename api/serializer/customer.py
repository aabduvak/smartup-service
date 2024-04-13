from rest_framework import serializers

from api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation["district"] and instance.district:
            representation["district"] = instance.district.name
        return representation
