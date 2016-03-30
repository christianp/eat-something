from django.shortcuts import render,redirect
from .models import MealCategory, Meal, Recipe
from . import forms
from django.views import generic
from django.core.urlresolvers import reverse

# Create your views here.

def index(request):
    context = {
        'categories': MealCategory.objects.all(),
    }
    return render(request,'index.html',context)

def random_meal_base(request):
    return redirect(reverse('random_meal',args=('main',)))

class RandomMeal(generic.DetailView):
    model = MealCategory
    template_name = 'random_meal.html'
    context_object_name = 'category'

    def get_context_data(self,**kwargs):
        context = super(RandomMeal,self).get_context_data(**kwargs)

        category = self.get_object()
        meal = category.random_meal()

        context['meal'] = meal
        return context

    def post(self,request,**kwargs):
        category = self.get_object()
        meal = Meal.objects.get(pk=request.POST.get('meal'))
        action = request.POST.get('action')

        if action=='reject':
            meal.weight *= 0.9
            meal.save()
            return redirect('random_meal',slug=category.slug)
        elif action=='accept':
            meal.weight *= 1.1
            meal.save()
            return redirect(meal.get_absolute_url())

class MealView(generic.DetailView):
    model = Meal
    template_name = 'meal/detail.html'
    context_object_name = 'meal'

class CreateMealView(generic.CreateView):
    model = Meal
    form_class = forms.Meal
    template_name = 'meal/create.html'

class UpdateMealView(generic.UpdateView):
    model = Meal
    form_class = forms.Meal
    template_name = 'meal/update.html'

class AddRecipeView(generic.CreateView):
    model = Recipe
    form_class = forms.Recipe
    template_name = 'meal/add_recipe.html'

    def dispatch(self,request,pk,*args):
        self.meal = Meal.objects.get(pk=pk)
        return super(AddRecipeView,self).dispatch(request,pk,*args)

    def get_initial(self,*args):
        data = super(AddRecipeView,self).get_initial(*args)
        data['meal'] = self.meal.pk
        return data

    def get_context_data(self,*args,**kwargs):
        context = super(AddRecipeView,self).get_context_data(*args,**kwargs)
        context['meal'] = self.meal
        return context

class DeleteMealView(generic.DeleteView):
    model = Meal
    template_name = 'meal/delete.html'

    def get_success_url(self):
        return reverse('index')

class DeleteRecipeView(generic.DeleteView):
    model = Recipe
    template_name = 'meal/delete.html'

    def get_success_url(self):
        return self.object.meal.get_absolute_url()

class UpdateRecipeView(generic.UpdateView):
    model = Recipe
    form_class = forms.Recipe
    template_name = 'meal/update_recipe.html'
