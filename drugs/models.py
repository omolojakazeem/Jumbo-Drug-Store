from django.conf import settings
from django.db import models
from django.urls import reverse


class DrugCategory(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class DrugItem(models.Model):
    drug_name = models.CharField(max_length=100)
    drug_category = models.ForeignKey(DrugCategory, on_delete=models.CASCADE)
    drug_man = models.CharField(max_length=100, blank=True, null=True)
    drug_size = models.CharField(max_length=10, blank=True, null=True)
    drug_thumbnail = models.ImageField(upload_to='drugs', blank=True, null=True)
    drug_composition = models.CharField(max_length=200, blank=True, null=True)
    drug_stock = models.IntegerField()
    drug_price = models.FloatField()
    drug_mfd = models.DateField()
    drug_exp = models.DateField()
    drug_available_since = models.DateTimeField(auto_now_add=True)
    drug_restocked_last = models.DateTimeField(auto_now=True)
    drug_added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('drugs:drug_detail', kwargs={
            'cat_name': self.drug_category,
            'pk':self.pk,
            'drug_name': self.drug_name,
        })

    @property
    def get_delete_url(self):
        return reverse('drugs:drug_delete', kwargs={
            'pk': self.pk,
            'cat_name': self.drug_category,
            'drug_name': self.drug_name
        })

    def __str__(self):
        return self.drug_name


