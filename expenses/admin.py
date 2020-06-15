from django.contrib import admin
from .models import Expenses, ExpensesCat
# Register your models here.

admin.site.register(ExpensesCat)
admin.site.register(Expenses)