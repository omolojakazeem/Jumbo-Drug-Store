from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import DrugItem
from .forms import DrugItemForm


class DrugListView(LoginRequiredMixin,ListView):
    model = DrugItem


class DrugCreateView(LoginRequiredMixin,CreateView):
    model = DrugItem
    form_class = DrugItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context


class DrugDetailView(LoginRequiredMixin,DetailView):
    model = DrugItem


class DrugUpdateView(LoginRequiredMixin,UpdateView):
    model = DrugItem
    form_class = DrugItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context


class DrugDeleteView(LoginRequiredMixin,DeleteView):
    model = DrugItem
    success_url = reverse_lazy('drugs:drug_list')
