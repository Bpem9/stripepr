from .models import *
from rest_framework import serializers

class OrderDetailSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(slug_field='name', queryset=Item.objects.all(), many=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id', 'items', 'total_price']

    def get_total_price(self, obj):
        return obj.items.aggregate(Sum('price'))['price__sum']


class OrderListSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(read_only=True, many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_total_price(self, obj):
        price = obj.items.aggregate(Sum('price'))['price__sum']
        if price:
            return str(price)
        return '0'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
