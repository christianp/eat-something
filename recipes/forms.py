from .models import Meal, Recipe
from django.forms import ModelForm, inlineformset_factory
from django import forms

class CreateRecipe(ModelForm):
    class Meta:
        model = Recipe
        fields = ('url','reference','ingredients','instructions','time')

class Meal(ModelForm):
    class Meta:
        model = Meal
        fields = ('name','description','category')
        widgets = {
            'category': forms.CheckboxSelectMultiple(),
        }

class CreateRecipe(ModelForm):
    class Meta:
        model = Recipe
        fields = ('meal','url','reference','ingredients','instructions','time')
        widgets = {
            'meal': forms.HiddenInput(),
        }
