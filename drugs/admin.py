from django.contrib import admin
from .models import DrugItem,DrugCategory


admin.site.register(DrugCategory)
admin.site.register(DrugItem)