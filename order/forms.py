from django import forms

from customers.models import Customer


class OrderForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())