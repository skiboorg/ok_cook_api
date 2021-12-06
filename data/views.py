from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *


class GetMenuType(generics.ListAPIView):
    serializer_class = MenuTypeSerializer
    queryset = MenuType.objects.all()


class GetCategory(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


