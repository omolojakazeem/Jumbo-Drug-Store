from django.contrib import admin
from .models import DrugOrderItem, DrugOrder


admin.site.register(DrugOrderItem)
admin.site.register(DrugOrder)