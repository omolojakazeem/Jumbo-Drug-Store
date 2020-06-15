import random
import string

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from order.models import DrugOrder

from .forms import CheckoutForm
from .models import Payment
from customers.models import Customer

from drugs.models import DrugItem


class OrderPayment(LoginRequiredMixin, ListView):
    model = Payment


def get_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=30))


class Checkout(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if 'customer' in request.session:
            session_customer = request.session['customer']
            try:
                order = DrugOrder.objects.get(
                    customer__customer_full_name=session_customer,
                    sold=False)
                initial = {
                    'order_amount':order.get_total_order_price,
                }
                form = CheckoutForm(request.POST or None, initial=initial)
                context = {
                    'form': form,
                    'orders': order,
                }
                return render(self.request, 'payment/checkout.html', context=context)
            except ObjectDoesNotExist:
                messages.info(self.request, "You do no have an active order")
                return redirect('drugs:drug_list')
        else:
            return redirect('order:initiate_order')

    def post(self, request, *args, **kwargs):
        if 'customer' in request.session:
            session_customer = request.session['customer']
            form = CheckoutForm(self.request.POST or None)

            try:
                order = DrugOrder.objects.get(
                    customer__customer_full_name=session_customer,
                    sold=False)

                if form.is_valid():
                    payment_option = form.cleaned_data.get('payment_option')
                    amount_collected = form.cleaned_data.get('amount_collected')
                    change_given = form.cleaned_data.get('change_given')
                    change_outstanding = form.cleaned_data.get('change_outstanding')
                    order_amount = form.cleaned_data.get('order_amount')
                    comment = form.cleaned_data.get('comment')

                    order_items = order.drug.all()
                    order_items.update(sold=True)

                    for drug in order_items:
                        my_drug = DrugItem.objects.get(drug_name=drug.drug.drug_name)
                        my_drug.drug_stock -= drug.quantity
                        my_drug.save()
                        drug.save()

                    create_payment = Payment.objects.create(
                        customer= Customer.objects.get(customer_full_name=session_customer),
                        payment_option=payment_option,
                        order_amount=order_amount,
                        amount_collected=amount_collected,
                        change_given=change_given,
                        change_outstanding=change_outstanding,
                        comment=comment,
                        attendant=request.user,
                        timestamp=timezone.now()
                    )

                    order.ordered = True
                    order.payment = create_payment
                    order.ref_code = get_ref_code()
                    order.sold_by = request.user
                    order.sold = True
                    order.save()

                    messages.info(self.request, "Payment Sucessful")
                    return redirect('drugs:drug_list')

                else:
                    messages.info(self.request, "Form Field not valid")
                    initial = {
                        'order_amount': order.get_total_order_price,
                    }
                    form = CheckoutForm(initial=initial)
                    return render(request,'drugs/drugitem_list.html',context={'form':form,})

            except ObjectDoesNotExist:
                #messages.info(self.request, "I do not exist")
                messages.info(self.request, "You do not have an active order")
                return redirect('payment:checkout')
        else:
            return redirect('order:initiate_order')