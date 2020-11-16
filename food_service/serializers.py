from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Food, OrderQuantity, Order


class SellerFoodSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)

    class Meta:
        model = Food
        fields = '__all__'
        read_only_fields = ['quantity_to_be_prepared', ]


class BuyerFoodSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)

    class Meta:
        model = Food
        fields = ['id', 'seller', 'name', 'price', 'image', 'category', 'discount', 'tax', 'labels']


class OrderQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderQuantity
        fields = ['food', 'quantity']

    def to_representation(self, instance):
        data = {
            'food': BuyerFoodSerializer(instance.food).data,
            'quantity': instance.quantity
        }
        return data


class OrderSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    components = OrderQuantitySerializer(many=True)

    class Meta:
        model = Order
        fields = ['buyer', 'components', 'delivered']

    def create(self, validated_data):
        components = validated_data.pop('components')
        order = Order.objects.create(**validated_data)
        for quantity in components:
            order_quantity = OrderQuantity.objects.create(**quantity)
            order.components.add(order_quantity.id)
        return order
