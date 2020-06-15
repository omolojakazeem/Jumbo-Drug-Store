from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import ExpensesForm
from .models import Expenses
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView


class ExpensesListView(LoginRequiredMixin,ListView):
    model = Expenses


class ExpensesDetailView(LoginRequiredMixin,DetailView):
    model = Expenses


class ExpensesUpdateView(LoginRequiredMixin,UpdateView):
    model = Expenses
    form_class = ExpensesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type':'Update',
        })
        return context


class ExpensesCreateView(LoginRequiredMixin,CreateView):
    model = Expenses
    form_class = ExpensesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type':'Create',
        })
        return context


class ExpensesDeleteView(LoginRequiredMixin,DeleteView):
    model = Expenses
    success_url = reverse_lazy('expenses:expense_list')
