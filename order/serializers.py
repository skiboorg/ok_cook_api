from rest_framework import serializers
from .models import *
from data.serializers import ItemSerializer,ComplectSerializer
from user.serializers import UserSerializer



class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=False, read_only=True)
    menu_type = ComplectSerializer(many=False, required=False, read_only=True)
    order_items = OrderItemSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'





