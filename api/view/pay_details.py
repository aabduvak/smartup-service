from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from api.models import PaymentType, Currency
from api.serializer.pay_details import PaymentTypeSerializer, CurrencySerializer

from api.utils.payment_type import create_payment_type, create_currency


class PaymentTypeListView(ListAPIView):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer


class CurrencyListView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CreateCurrencyView(APIView):
    permission_classes = [
        IsAdminUser,
    ]

    def post(self, request):
        if not create_currency():
            return Response(
                {
                    "status": "error",
                    "message": "error occured while creating currencies",
                },
                status=500,
            )

        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)

        return Response(serializer.data, status=200)


class CreatePaymentTypeView(APIView):
    permission_classes = [
        IsAdminUser,
    ]

    def post(self, request):

        if not create_payment_type():
            return Response(
                {
                    "status": "error",
                    "message": "error occured while creating payment-types",
                },
                status=500,
            )
        payment_types = PaymentType.objects.all()
        serializer = PaymentTypeSerializer(payment_types, many=True)
        return Response(serializer.data)
