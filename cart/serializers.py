from rest_framework import serializers
from .models import *
from data.serializers import ItemSerializer, ComplectSerializer


class CartComplectItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = CartComplectItem
        fields = '__all__'

class CartComplectSerializer(serializers.ModelSerializer):
    items = CartComplectItemSerializer(many=True, required=False, read_only=True)
    complect = ComplectSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = CartComplect
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, required=False, read_only=True)
    complects = CartComplectSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'




