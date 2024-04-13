from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.conf import settings
from datetime import date

from api.models import Product
from api.serializer.product import ProductSerializer
from api.utils.product import create_product, create_products

BRANCHES_ID = settings.BRANCHES_ID


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
    permission_classes = [
        IsAdminUser,
    ]

    def post(self, request):
        branches = BRANCHES_ID

        if "branch" in request.data:
            branches = [request.data["branch"]]

        for branch in branches:
            if not create_products(branch):
                return Response(
                    {
                        "status": "error",
                        "message": "error occured while creating products",
                    },
                    status=500,
                )

        today = date.today()

        products = Product.objects.filter(created_at__date=today)
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data)
