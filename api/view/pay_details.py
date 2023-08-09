from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import PaymentType, Currency
from api.serializer.pay_details import PaymentTypeSerializer, CurrencySerializer
from api.utils.get_data import get_data

class PaymentTypeListView(ListAPIView):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

class CurrencyListView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class CreateCurrencyView(APIView):
    def get(self, request):
        if 'Sessionid' not in request.headers:
            return Response(status=401)
        
        session = request.headers['Sessionid']
        columns = [
            "name",
            "state_name",
            "currency_id"
        ]
        
        response = get_data(endpoint='/b/anor/mk/currency_list+x&table', session=session, columns=columns)
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
        return_data = [{"id": currency.id, "name": currency.name, 'created_at': currency.created_at} for currency in currencies]
        
        return Response(return_data, status=200)

class CreatePaymentTypeView(APIView):
    def get(self, request):
        if 'Sessionid' not in request.headers:
            return Response(status=401)
        
        session = request.headers['Sessionid']
        columns = [
            "payment_type_id",
            "name",
            "currency_name"
        ]
        
        response = get_data(endpoint='/b/anor/mkr/payment_type_list+x&table', session=session, columns=columns, remove_parent=True)
        if not response:
            return Response(status=500)
        payment_types = response['data']
        
        try:    
            for data in payment_types:
                if not PaymentType.objects.filter(smartup_id=data[0]).exists():
                    currency = Currency.objects.get(name=data[2])
                    
                    PaymentType.objects.create(
                        smartup_id=data[0],
                        name=data[1],
                        currency=currency
                    )
        except:
            return Response(status=500)
    
        payment_types = PaymentType.objects.all()
        return_data = [{"id": data.id, "smartup_id": data.smartup_id, "name": data.name, 'created_at': data.created_at} for data in payment_types]
        
        return Response(return_data, status=200)
