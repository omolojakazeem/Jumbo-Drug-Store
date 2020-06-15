from django import forms
from django.forms import ModelForm, ChoiceField

from payment.models import Payment

PAYMENT_TYPE = (
        ('CASH', 'CASH'),
        ('TRANSFER', 'TRANSFER'),
    )


class CheckoutForm(ModelForm):
    payment_option = forms.ChoiceField(choices=PAYMENT_TYPE)

    class Meta:
        model = Payment
        fields = ('payment_option','order_amount', 'amount_collected', 'change_given','comment')



