from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Customer
from .forms import CustomerForm


class CustomerListView(LoginRequiredMixin,ListView):
    model = Customer


class CustomerCreateView(LoginRequiredMixin,CreateView):
    model = Customer
    form_class = CustomerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('customer:customer_list')
