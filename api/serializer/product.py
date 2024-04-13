from rest_framework.serializers import ModelSerializer
from api.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation["brand"] and instance.brand:
            representation["brand"] = instance.brand.name

        return representation
