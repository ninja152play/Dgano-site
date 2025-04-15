from rest_framework import serializers

from order.models import *
from product.serializers import ProductShortSerializer


class OrderSerializer(serializers.ModelSerializer):
    products = ProductShortSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

