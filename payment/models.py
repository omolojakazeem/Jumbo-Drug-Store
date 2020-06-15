from django.conf import settings
from django.db import models

# Create your models here.
from customers.models import Customer


PAYMENT_TYPE = (
        ('CASH', 'CASH'),
        ('TRANSFER', 'TRANSFER'),
    )


class Payment(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    payment_option = models.CharField(choices=PAYMENT_TYPE, max_length=10)
    order_amount = models.FloatField()
    amount_collected = models.FloatField()
    change_given = models.FloatField(blank=True, null=True, default=0)
    change_outstanding = models.FloatField(blank=True, null=True, default=0)
    comment = models.TextField(blank=True)
    attendant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.customer_full_name