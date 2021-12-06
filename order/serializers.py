from rest_framework import serializers
from .models import *
from data.serializers import ItemSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'





