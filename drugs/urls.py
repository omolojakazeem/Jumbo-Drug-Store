from django.urls import path
from .views import DrugListView, DrugDetailView, DrugUpdateView, DrugDeleteView, DrugCreateView

app_name = 'drugs'

urlpatterns = [
    path('',DrugListView.as_view(), name = 'drug_list'),
    path('create/',DrugCreateView.as_view(), name = 'drug_create'),
    path('details/<cat_name>/<drug_name>/<pk>/',DrugDetailView.as_view(), name = 'drug_detail'),
    path('update/<cat_name>/<drug_name>/<pk>/',DrugUpdateView.as_view(), name = 'drug_update'),
    path('delete/<cat_name>/<drug_name>/<pk>/',DrugDeleteView.as_view(), name = 'drug_delete')
]