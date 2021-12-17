from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *

class GetComplect(generics.RetrieveAPIView):
    serializer_class = ComplectSerializer

    def get_object(self):
        print(self.request.query_params.get('id'))
        return Complect.objects.filter(id=self.request.query_params.get('id')).first()

class GetComplects(generics.ListAPIView):
    serializer_class = ComplectSerializer
    queryset = Complect.objects.all()


class GetCategory(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


