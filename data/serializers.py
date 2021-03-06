from rest_framework import serializers
from .models import *


class ComplectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complect
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'





