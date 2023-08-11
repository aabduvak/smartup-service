from rest_framework.serializers import ModelSerializer
from api.models import Payment, User, PaymentType

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['customer'] and instance.customer:
            representation['customer'] = instance.customer.name
        if representation['payment_type'] and instance.payment_type:
            representation['payment_type'] = instance.payment_type.name
        if representation['branch'] and instance.branch:
            representation['branch'] = instance.branch.name
        
        representation['currency'] = instance.payment_type.currency.name
        return representation
