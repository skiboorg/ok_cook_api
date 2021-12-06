from rest_framework import serializers
from .models import *
from data.serializers import ItemSerializer

class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'





