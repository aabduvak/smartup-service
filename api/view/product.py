from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Product
from api.serializer.product import ProductSerializer

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductListView(APIView):
    def get(self, request, code):
        if code is None:
            return Response(status=400)
        
        if not Product.objects.filter(code=code).exists():
            product = create_product(code)
            
            if not product:
                return Response(status=404)
        
        product = Product.objects.get(code=code)
        serializer = ProductSerializer(product)
        return Response(serializer.data)     