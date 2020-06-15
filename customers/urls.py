from django.urls import path
from .views import CustomerCreateView, CustomerDeleteView, CustomerDetailView, CustomerListView, CustomerUpdateView

app_name = 'customer'

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer_list'),
    path('create/', CustomerCreateView.as_view(), name='customer_create'),
    path('details/<customer_name>/<pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('update/<customer_name>/<pk>/', CustomerUpdateView.as_view(), name='customer_update'),
    path('delete/<customer_name>/<pk>/', CustomerDeleteView.as_view(), name='customer_delete')
]
