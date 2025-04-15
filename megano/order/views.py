from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from order.models import *
from order.serializers import *
from product.serializers import ProductShortSerializer
from product.models import Basket

# Create your views here.
class OrdersView(APIView):
    def get(self, request):
        user = request.user
        user = Profile.objects.get(user=user)
        orders = Order.objects.filter(user=user).all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            user = request.user
            user = Profile.objects.get(user=user)
            data = request.data.copy()
            order = Order.objects.create(user=user, status='created')
            totalCost = 0
            for product in data:
                prd = Product.objects.get(pk=product['id'])
                count = product['count']
                OrderProductCount.objects.create(order=order, product=prd, count=count)
                totalCost += count * prd.price
            order.totalCost = totalCost
            order.save()
            return Response({"orderId": order.id}, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderView(APIView):
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            contener = OrderProductCount.objects.filter(order=order).all()
            products = []
            counts = []
            for i in contener:
                products.append(Product.objects.get(pk=i.product.id))
                counts.append(i.count)
            order.products.set(products)
            serializer = OrderSerializer(order)
            for i in range(len(serializer.data['products'])):
                serializer.data['products'][i]['count'] = counts[i]
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, pk):
        data = request.data.copy()
        order = Order.objects.get(pk=pk)
        payment = Payment.objects.create(order=order)
        order.fullName = data['fullName']
        order.phone = data['phone']
        order.email = data['email']
        if not data['deliveryType'] == None:
            order.deliveryType = data['deliveryType']
        order.city = data['city']
        order.address = data['address']
        if not data['paymentType'] == None:
            order.paymentType = data['paymentType']
        order.status = 'waiting for payment'
        order.save()
        return Response({"orderId": order.id}, status=status.HTTP_200_OK)


class PaymentView(APIView):
    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            payment = Payment.objects.get(order=order)
            payment.name = request.data['name']
            payment.number = request.data['number']
            payment.year = request.data['year']
            payment.month = request.data['month']
            payment.code = request.data['code']
            payment.save()
            order.status = 'paid'
            order.save()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)