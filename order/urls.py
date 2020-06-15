from django.urls import path

from .views import (
    OrderListView,
    order_list_view,
    pre_sale,
    add_to_cart,
    OrderSummaryView,
    remove_from_cart,
    remove_single_item_from_cart,
    order_invoice,
html_to_pdf_view,)

app_name = 'order'

urlpatterns = [
    #path('', OrderListView.as_view(), name='order_list'),
    path('', order_list_view, name='order_list'),
    path('initiate_order/', pre_sale, name='initiate_order'),
    path('print_invoice/<pk>', html_to_pdf_view, name='print_invoice'),
    path('add_to_cart/<name>', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<name>', remove_single_item_from_cart, name='remove_from_cart'),
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('delete_order/<name>', remove_from_cart, name='delete_order'),
    path('order_invoice/<pk>', order_invoice, name='order_invoice'),

]
