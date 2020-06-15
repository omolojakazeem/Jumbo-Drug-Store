from django.urls import path

from .views import Checkout, OrderPayment

app_name = 'payment'

urlpatterns = [
    path('', OrderPayment.as_view(), name = 'payment_list'),
    path('checkout/', Checkout.as_view(), name = 'checkout')
]