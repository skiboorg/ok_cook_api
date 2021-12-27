from rest_framework import serializers
from .models import *
from data.serializers import ItemSerializer,ComplectSerializer
from user.serializers import UserSerializer

class OrderCitySectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCitySector
        fields = '__all__'


class OrderCitySerializer(serializers.ModelSerializer):
    sectors = OrderCitySectorSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = OrderCity
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=False, read_only=True)
    city = OrderCitySerializer(many=False, required=False, read_only=True)
    sector = OrderCitySectorSerializer(many=False, required=False, read_only=True)
    menu_type = ComplectSerializer(many=False, required=False, read_only=True)
    order_items = OrderItemSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'





