from django.contrib import admin

from .models import MealCategory,Meal,Recipe

class RecipeInline(admin.StackedInline):
    model = Recipe
    min_num = 1
    extra = 1

class MealAdmin(admin.ModelAdmin):
    model = Meal
    inlines = (RecipeInline,)

# Register your models here.
admin.site.register(MealCategory)
admin.site.register(Meal, MealAdmin)
admin.site.register(Recipe)
