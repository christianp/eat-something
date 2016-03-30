from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'random$',views.random_meal_base,name='random_meal_base'),
    url(r'random/(?P<slug>[^/]+)$',views.RandomMeal.as_view(),name='random_meal'),
    url(r'^meal/new$',views.CreateMealView.as_view(),name='meal_create'),
    url(r'^meal/(?P<pk>\d+)$', views.MealView.as_view(), name='meal'),
    url(r'^meal/(?P<pk>\d+)/edit$', views.UpdateMealView.as_view(), name='meal_edit'),
    url(r'^meal/(?P<pk>\d+)/add_recipe$', views.AddRecipeView.as_view(), name='meal_add_recipe'),
    url(r'^meal/(?P<pk>\d+)/delete$', views.DeleteMealView.as_view(), name='meal_delete'),
    url(r'^recipe/(?P<pk>\d+)/delete$', views.DeleteRecipeView.as_view(), name='recipe_delete'),
    url(r'^recipe/(?P<pk>\d+)/edit$', views.UpdateRecipeView.as_view(), name='recipe_edit'),
]
