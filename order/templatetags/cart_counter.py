from django import template
from django.contrib.messages.storage import session

from ..models import DrugOrder

register = template.Library()


@register.simple_tag
def cart_item_count(customer):
    if customer:
        qs = DrugOrder.objects.filter(sold=False, customer__customer_full_name=customer)
        if qs.exists():
            my_cart_counter = qs[0].drug.count()
            return my_cart_counter
    return 0