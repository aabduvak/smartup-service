from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import PaymentType, Currency
from api.serializer.pay_details import PaymentTypeSerializer, CurrencySerializer

from api.utils.get_data import get_data
from api.utils.payment_type import create_payment_type

class PaymentTypeListView(ListAPIView):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

class CurrencyListView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class CreateCurrencyView(APIView):
    def post(self, request):
        columns = [
            "name",
            "state_name",
            "currency_id"
        ]
        
        response = get_data(endpoint='/b/anor/mk/currency_list+x&table', columns=columns)
        if not response:
            return Response(status=500)
        currencies = response['data']
       
        try:    
            for currency in currencies:
                if not Currency.objects.filter(name=currency[0]).exists():
                    Currency.objects.create(
                        name=currency[0]
                    )
        except:
            return Response(status=500)
    
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        
        return Response(serializer.data, status=200)

class CreatePaymentTypeView(APIView):
    def post(self, request):

        if create_payment_type():
            payment_types = PaymentType.objects.all()
            serializer = PaymentTypeSerializer(payment_types, many=True)
            return Response(serializer.data)
        return Response(status=500)
        