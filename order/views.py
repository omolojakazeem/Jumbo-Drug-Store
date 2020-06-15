import random
import string

from customers.models import Customer
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from drugs.models import DrugItem
from order.models import DrugOrder
from order.models import DrugOrderItem
from weasyprint import HTML, CSS

from .forms import OrderForm


def get_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


@login_required
def order_list_view(request):
    template = 'order/drugorder_list.html'
    if request.method == 'GET':
        active_order = DrugOrder.objects.filter(sold=False)
        closed_order = DrugOrder.objects.filter(sold=True)

        context = {
            'active_orders': active_order,
            'closed_orders': closed_order,
        }
        return render(request, template_name=template, context=context)


class OrderListView(LoginRequiredMixin, ListView):
    model = DrugOrder


def order_item_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


@login_required
def pre_sale(request, ):
    if request.method == 'GET':

        form = OrderForm(request.POST)
        context = {
            'form': form,
        }
        return render(request, 'order/pre-sale.html', context=context)

    else:
        form = OrderForm(request.POST or None)
        if form.is_valid():
            form_customer = form.cleaned_data['customer']
            the_customer = Customer.objects.get(customer_full_name=form_customer)
            request.session['customer'] = the_customer.customer_full_name
            messages.info(request, f"Customer Set-{request.session['customer']}")
            return redirect('drugs:drug_list')
        else:

            form = OrderForm()
        return render(request, 'drugs/drugitem_list.html', context={'form': form, })


@login_required
def add_to_cart(request, name):
    stock_status = DrugItem.objects.all().count()
    if stock_status > 0:
        if 'customer' in request.session:
            session_customer = request.session['customer']
            my_drug = get_object_or_404(DrugItem, drug_name=name)
            my_customer = Customer.objects.get(customer_full_name=session_customer)

            order_item, created = DrugOrderItem.objects.get_or_create(
                customer=my_customer,
                drug=my_drug,
                sold=False)
            order_qs = DrugOrder.objects.filter(customer=my_customer, sold=False)

            if order_qs.exists():
                order = order_qs[0]

                if order_item.quantity < stock_status:
                    if order.drug.filter(drug__drug_name=my_drug.drug_name).exists():
                        order_item.quantity += 1
                        order_item.save()
                        order.drug.add(order_item)
                        messages.info(request, f"The quantity of this Item {order_item} was updated in your cart")
                        return redirect('order:order_summary')

                    else:
                        order.drug.add(order_item)
                        messages.info(request, f"This Item '{order_item}' was added to your cart")
                        return redirect('drugs:drug_list')
                else:
                    messages.info(request, "Stock too Low")
                    return redirect('order:order_summary')
            else:
                ordered_date = timezone.now()
                order = DrugOrder.objects.create(customer=my_customer, ordered_date=ordered_date)
                order.drug.add(order_item)
                messages.info(request, f"This Item {order_item}'s quantity was updated in your cart")

                return redirect('drugs:drug_list')
        else:
            return redirect('order:initiate_order')
    else:
        messages.info(request, "Stock too Low")
        return redirect('drugs:drug_list')


@login_required
def remove_single_item_from_cart(request, name):
    if 'customer' in request.session:
        drug = get_object_or_404(DrugItem, drug_name=name)
        session_customer = request.session['customer']
        order_qs = DrugOrder.objects.filter(customer__customer_full_name=session_customer, sold=False)

        if order_qs.exists():
            order = order_qs[0]

            if order.drug.filter(drug__drug_name=drug.drug_name).exists():
                order_item = DrugOrderItem.objects.filter(
                    drug=drug,
                    customer=Customer.objects.get(customer_full_name=session_customer),
                    sold=False)[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                else:
                    order.drug.remove(order_item)
                messages.info(request, "The quantity of this item was updated in your cart")
                return redirect('order:order_summary')
            else:
                messages.info(request, "This Item does not exist in your cart")
                return redirect('order:order_summary')

        else:
            messages.info(request, "You do not have an active order")
            return redirect('drugs:drug_list')
    else:
        return redirect('order:initiate_order')


@login_required
def remove_from_cart(request, name):
    if 'customer' in request.session:
        drug = get_object_or_404(DrugItem, drug_name=name)
        session_customer = request.session['customer']
        order_qs = DrugOrder.objects.filter(customer__customer_full_name=session_customer, sold=False)

        if order_qs.exists():
            order = order_qs[0]

            if order.drug.filter(drug__drug_name=drug.drug_name).exists():
                order_item = DrugOrderItem.objects.filter(
                    drug=drug,
                    customer=Customer.objects.get(customer_full_name=session_customer),
                    sold=False)[0]
                order.drug.remove(order_item)
                messages.info(request, "This Item was removed from your cart")
                return redirect('order:order_summary')
            else:
                messages.info(request, "This Item does not exist in your cart")
                return redirect('drugs:drug_list')
        else:
            messages.info(request, "You do not have an active order")
            return redirect('drugs:drug_list')
    else:
        return redirect('order:initiate_order')


class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if 'customer' in request.session:
            session_customer = request.session['customer']
            try:
                order = DrugOrder.objects.get(customer__customer_full_name=session_customer, sold=False)
                context = {
                    'object': order,
                }

                return render(self.request, 'order/order_summary.html', context=context)
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("drugs:drug_list")
        else:
            return redirect('order:initiate_order')


@login_required
def order_invoice(request, pk):
    if request.method == 'GET':
        order = DrugOrder.objects.get(pk=pk)
        template = 'order/invoice-page.html'

        context = {
            'order': order,
        }
        return render(request, template_name=template, context=context)


@login_required
def html_to_pdf_view(request, pk):
    order = DrugOrder.objects.get(pk=pk)
    context = {
        'order': order,
    }
    html_template = render_to_string('order/invoice.html', context=context)
    pdf_file = HTML(string=html_template).write_pdf(
        stylesheets=[CSS(settings.STATIC_ROOT + '/css/invoice.css')]
    )
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="invoice.pdf"'
    return response
