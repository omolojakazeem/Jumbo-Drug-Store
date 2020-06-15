from django.conf import settings
from django.db import models

from django.urls import reverse


class ExpensesCat(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Expenses(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(ExpensesCat, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    spent_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('expenses:expense_detail', kwargs={
            'exp_cat':self.category,
            'exp_title': self.title,
            'pk':self.pk,
        })


    def __str__(self):
        return self.title