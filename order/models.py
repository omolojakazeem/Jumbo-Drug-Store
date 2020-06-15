from customers.models import Customer
from django.conf import settings
from django.db import models
from drugs.models import DrugItem


# Create your models here.
from payment.models import Payment


class DrugOrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    drug = models.ForeignKey(DrugItem, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    sold = models.BooleanField(default=False)

    @property
    def get_total_drug_price(self):
        return round(self.drug.drug_price * self.quantity, 2)

    def __str__(self):
        return f"{self.quantity} of {self.drug.drug_name}"


class DrugOrder(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    sold = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=50,)
    drug = models.ManyToManyField(DrugOrderItem)
    ordered_date = models.DateTimeField()
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True,blank=True)
    sold_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    @property
    def get_total_order_price(self):
        total = 0
        for drug_item in self.drug.all():
                total += drug_item.get_total_drug_price
        return round(total, 2)

    def __str__(self):
        return self.customer.customer_full_name