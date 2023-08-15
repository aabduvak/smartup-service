from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Product, Branch, Brand
from api.serializer.product import ProductSerializer
from api.utils.product import create_product
from api.utils.get_data import get_json_data

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(APIView):
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

class CreateProductView(APIView):
    def post(self, request):
        if not 'branch' in request.data:
            return Response(status=400)
        
        if not Branch.objects.filter(smartup_id=request.data['branch']).exists():
            return Response(status=404)
        
        branch = Branch.objects.get(smartup_id=request.data['branch'])
        products = get_json_data(endpoint='/b/es/porting+exp$se_product', branch=branch.smartup_id)
        
        for product in products:
            if Product.objects.filter(code=product['code']).exists():
                continue
            
            new_product = Product.objects.create(
                    code=product['code'],
                    smartup_id=product['product_id'],
                    name=product['name']
                )
            
            if product['ikpu'] != "":
                new_product.fiskal_code = product['ikpu']
                
            if len(product['barcodes']) >= 1:
                new_product.barcode = product['barcodes'][0]
            
            if Brand.objects.filter(name=product['producer_name']).exists():
                brand = Brand.objects.get(name=product['producer_name'])
                new_product.brand = brand
            new_product.save()
        
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data)