from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from api.models import User, Deal
from api.serializer.deal import DealSerializer