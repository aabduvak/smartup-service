from datetime import datetime
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.conf import settings
from datetime import datetime

from api.serializer.payment import PaymentSerializer
from api.models import Payment, Branch, User
from api.utils.payment import create_payments

BRANCHES_ID = settings.BRANCHES_ID

class PaymentListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        queryset = Payment.objects.all()
        
        user_id = self.request.query_params.get('customer')
        branch = self.request.query_params.get('branch')
        date = self.request.query_params.get('date')
        currency = self.request.query_params.get('currency')
        payment_type = self.request.query_params.get('payment_type')
                
        if user_id and User.objects.filter(smartup_id=user_id).exists():
            queryset = queryset.filter(customer__smartup_id=user_id)
        
        if branch and Branch.objects.filter(smartup_id=branch).exists():
            queryset = queryset.filter(branch__smartup_id=branch)
        
        if date:
            date_of_payment = datetime.strptime(date, '%d.%m.%Y')
            queryset = queryset.filter(date_of_payment=date_of_payment.strftime('%Y-%m-%d'))
        
        if currency:
            queryset = queryset.filter(payment_type__currency__name=currency)
        
        if payment_type:
            queryset = queryset.filter(payment_type__smartup_id=payment_type)
        
        return queryset

class PaymentDetailView(APIView):
    def get(self, request, smartup_id):
        if not smartup_id:
            return Response({'error':'smartup_id is required'}, status=400)
        
        if not Payment.objects.filter(smartup_id=smartup_id).exists():
            return Response({'error':'payment not found'}, status=404)
        
        payment = Payment.objects.get(smartup_id=smartup_id)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

class CreatePaymentView(APIView):
    def post(self, request):
        branches = BRANCHES_ID
        date = datetime.now().strftime('%d.%m.%Y')
        
        if 'branch' in request.data:
            branches = [request.data['branch']]
        
        if 'date' in request.data:
            date = request.data['date']
        
        for branch in branches:
            if not create_payments(branch, date):
                return Response({'status':'error', 'message': 'error occured while creating payments'}, status=500)
        
        date_of_payment = datetime.strptime(date, '%d.%m.%Y').date()
        
        payments = Payment.objects.filter(date_of_payment=date_of_payment)
        serializer = PaymentSerializer(payments, many=True)
        return Response({'status':'success', 'result': serializer.data}, status=200)