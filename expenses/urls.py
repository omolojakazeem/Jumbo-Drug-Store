from django.urls import path

from .views import (
    ExpensesDetailView,
    ExpensesCreateView,
    ExpensesDeleteView,
    ExpensesListView,
    ExpensesUpdateView)

app_name ='expenses'

urlpatterns = [
    path('', ExpensesListView.as_view(), name = 'expense_list'),
    path('create/', ExpensesCreateView.as_view(), name = 'expense_create'),
    path('detail/<exp_cat>/<exp_title>/<pk>/', ExpensesDetailView.as_view(), name = 'expense_detail'),
    path('update/<exp_cat>/<exp_title>/<pk>/', ExpensesUpdateView.as_view(), name = 'expense_update'),
    path('delete/<exp_cat>/<exp_title>/<pk>/', ExpensesDeleteView.as_view(), name = 'expense_delete'),
]