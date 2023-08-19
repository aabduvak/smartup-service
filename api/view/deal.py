from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.conf import settings
from datetime import datetime, date

from api.models import Deal, OrderDetails
from api.serializer.deal import DealSerializer
from api.utils.deal import create_deals

BRANCHES_ID = settings.BRANCHES_ID

class DealListView(ListAPIView):
    serializer_class = DealSerializer
    queryset = Deal.objects.all()

class DealDetailView(APIView):
    def get(self, request, smartup_id):
        if not smartup_id:
            return Response(status=400)
        
        if not Deal.objects.filter(smartup_id=smartup_id).exists():
            return Response(status=404)
        
        deal = Deal.objects.get(smartup_id=smartup_id)
        details = OrderDetails.objects.filter(deal=deal)
        serializer = DealSerializer(deal)
        data = serializer.data
        products = []
        for detail in details:
            product = {
                "name": detail.product.name,
                "code": detail.product.code,
                "brand": detail.product.brand.name,
                "quantity": detail.quantity,
                "price": detail.unit_price,
            }
            
            products.append(product)

        data['products'] = products
        return Response(data)

class CreateDealView(APIView):
    def post(self, request):
        branches = BRANCHES_ID
        date_deal = datetime.now().strftime('%d.%m.%Y')
        
        if 'branch' in request.data:
            branches = [request.data['branch']]
        
        if 'date' in request.data:
            date_deal = request.data['date']
            
        for branch in branches:
            if not create_deals(branch, date_deal):
                return Response({'status':'error', 'message': 'error occured while creating deals'}, status=500)
        
        today = date.today()
        
        deals = Deal.objects.filter(created_at__date=today)
        serializer = DealSerializer(deals, many=True)
        return Response({'status':'success', 'result': serializer.data}, status=200)