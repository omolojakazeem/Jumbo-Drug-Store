from django.forms import ModelForm
from .models import DrugItem, DrugCategory


class DrugItemForm(ModelForm):
    class Meta:
        model = DrugItem
        fields = ('__all__')


class DrugCategoryForm(ModelForm):
    class Meta:
        model = DrugCategory
        fields = ('__all__')

