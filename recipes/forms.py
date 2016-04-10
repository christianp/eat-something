from .models import Meal, Recipe
from django.forms import ModelForm, inlineformset_factory
from django import forms
from django.utils import dateparse
import re
import datetime
from django.utils.html import conditional_escape, format_html, html_safe

class ButtonChoiceInput(forms.widgets.CheckboxChoiceInput):
    def render(self, name=None, value=None, attrs=None):
        if self.id_for_label:
            label_for = format_html(' for="{}"', self.id_for_label)
        else:
            label_for = ''
        attrs = dict(self.attrs, **attrs) if attrs else self.attrs
        return format_html(
            '<label{}>{} <span class="btn large full-width">{}</span></label>', label_for, self.tag(attrs), self.choice_label
        )

class ButtonFieldRenderer(forms.widgets.ChoiceFieldRenderer):
    choice_input_class = ButtonChoiceInput
    outer_html = '<ul{id_attr} class="button-choice-input">{content}</ul>'

class ButtonSelectMultiple(forms.CheckboxSelectMultiple):
    renderer = ButtonFieldRenderer

class CreateRecipe(ModelForm):
    class Meta:
        model = Recipe
        fields = ('url','reference','ingredients','instructions','time')

class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ('name','description','category')
        widgets = {
            'category': ButtonSelectMultiple(),
        }

class CreateMealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ('name','description','category','added_by')
        widgets = {
            'added_by': forms.HiddenInput(),
            'category': ButtonSelectMultiple(),
        }

english_duration_re = re.compile(r'\s*(?:,|and)?\s*(?P<amount>\d+) ?(?P<unit>day|d|hour|h|minute|min|m|second|s)s?')
english_duration_all_re = re.compile('^(?:{})+$'.format(english_duration_re.pattern))
time_unit_translation = {
    'day': 'day',
    'd': 'day',
    'hour': 'hour',
    'h': 'hour',
    'minute': 'minute',
    'min': 'minute',
    'm': 'minute',
    'second': 'second',
    's': 'second',
}

def parse_duration(value):
    value = value.strip()
    if english_duration_all_re.match(value):
        days = 0
        seconds = 0
        d = {}
        for m in english_duration_re.finditer(value):
            unit = m.group('unit')
            unit = time_unit_translation[unit]
            amount = m.group('amount')
            d[unit+'s'] = float(amount)
        return datetime.timedelta(**d)
    else:
        return dateparse.parse_duration(value)


class CleverDurationField(forms.DurationField):
    def to_python(self,value):
        if value in self.empty_values:
            return None
        if isinstance(value, datetime.timedelta):
            return value
        value = parse_duration(value)
        if value is None:
            raise forms.ValidationError(self.error_messages['invalid'], code='invalid')
        return value

class RecipeForm(ModelForm):
    time = CleverDurationField()
    class Meta:
        model = Recipe
        fields = ('meal','url','reference','ingredients','instructions','time')
        widgets = {
            'meal': forms.HiddenInput(),
        }

class CreateRecipeForm(ModelForm):
    time = CleverDurationField()
    class Meta:
        model = Recipe
        fields = ('meal','url','reference','ingredients','instructions','time','added_by')
        widgets = {
            'meal': forms.HiddenInput(),
            'added_by': forms.HiddenInput(),
        }
