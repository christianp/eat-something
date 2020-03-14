from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from random import random
from .ingredient_parser import html_ingredients

class MealCategory(models.Model):
    name = models.CharField(max_length=254)
    slug = models.SlugField(editable=False,default='')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def random_meal(self):
        total = self.meals.aggregate(total=models.Sum('weight'))['total']
        r = random()*total
        acc = 0
        for meal in self.meals.all():
            acc += meal.weight
            if acc >= r:
                return meal

    def get_absolute_url(self):
        return reverse('index')

@receiver(models.signals.pre_save,sender=MealCategory)
def set_slug_pre_save(sender,instance,**kwargs):
    instance.slug = slugify(instance.name)

# Create your models here.
class Meal(models.Model):
    category = models.ManyToManyField(MealCategory,related_name='meals')
    emoji = models.CharField(max_length=12,blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    weight = models.FloatField(default=1)
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('meal',args=(self.pk,))

    @property
    def time(self):
        if self.recipes.exists():
            return self.recipes.all().aggregate(time=models.Min('time'))['time']
        else:
            return None

class Recipe(models.Model):
    meal = models.ForeignKey(Meal,related_name='recipes',on_delete=models.CASCADE)
    url = models.URLField(blank=True,help_text='URL of the recipe')
    reference = models.CharField(max_length=254,blank=True,help_text='A page number in a book')
    ingredients = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    time = models.DurationField()
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return 'Recipe for {}'.format(self.meal.name)

    def ingredients_list(self):
        return self.ingredients.split('\n')

    def get_absolute_url(self):
        return reverse('meal',args=(self.pk,))

    def get_absolute_url(self):
        return reverse('meal',args=(self.meal.pk,))

    def nice_ingredients(self):
        return html_ingredients(self.ingredients)
