from django.forms.models import ModelForm
from base.prodserv_models import Measure, Ingredients, Category, Position, Worker, Service

__author__ = 'maykel'

from django import forms

class IngredientsForm(ModelForm):
    # measure = forms.ModelChoiceField(queryset=Measure.objects.all())
    class Meta:
        model = Ingredients
        fields = ['name', 'description']



class RecipesForm(forms.Form):
    name = forms.CharField(max_length=250, required=True)
    ingredients = forms.ModelChoiceField(required=True, queryset=Ingredients.objects.all())
    measure  = forms.ModelChoiceField(required=True, queryset=Measure.objects.all())
    cant = forms.IntegerField(required=True)

class ProdForm(ModelForm):
    class Meta:
        model = Ingredients
        fields = ['name', 'description']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['description']

class PositionForm(ModelForm):
    class Meta:
        model = Position
        fields = ['description']
class WorkerForm(ModelForm):
    class Meta:
        model = Worker
        fields = ['name', 'last_name']
class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'tarifa_horaria']




