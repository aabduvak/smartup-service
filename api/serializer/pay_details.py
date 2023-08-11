from rest_framework.serializers import ModelSerializer
from api.models import Currency, PaymentType

class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class PaymentTypeSerializer(ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['currency'] and instance.currency:
            representation['currency'] = instance.currency.name
        return representation
