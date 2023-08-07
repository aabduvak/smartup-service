from rest_framework.generics import ListAPIView
from api.models import PaymentType, Currency

from api.serializer.pay_details import PaymentTypeSerializer, CurrencySerializer

class PaymentTypeListView(ListAPIView):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

class CurrencyListView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

