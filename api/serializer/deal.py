from rest_framework.serializers import ModelSerializer

from api.models import Deal


class DealSerializer(ModelSerializer):
    class Meta:
        model = Deal
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation["customer"] and instance.customer:
            representation["customer"] = instance.customer.name
        if representation["payment_type"] and instance.payment_type:
            representation["payment_type"] = instance.payment_type.name
        if representation["payment_type"] and instance.payment_type:
            representation["currency"] = instance.payment_type.currency.name
        return representation
