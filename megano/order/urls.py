from django.urls import path
from order.views import *

urlpatterns = [
    path('orders', OrdersView.as_view(), name='orders'),
    path('order/<int:pk>', OrderView.as_view(), name='order'),
    path('payment/<int:pk>', PaymentView.as_view(), name='payment')
]