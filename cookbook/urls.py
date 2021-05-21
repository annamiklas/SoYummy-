from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'cookbook'

urlpatterns = [
    path('recipes/', views.recipes_page, name='recipes'),
    path('recipes/<slug:category_slug>/', views.recipes_page, name='recipe_category'),
    path('edit_recipe/<str:idR>', views.edit_recipe_page, name="edit_recipe"),
    path('recipe/<str:idR>', views.recipe_page, name="recipe"),
    path('delete_recipe/<str:idR>', views.delete_recipe, name="delete_recipe"),
    path('create_recipe/', views.create_recipe_page, name="create_recipe"),
    path('submit_rating/<str:idR>', views.submit_rating, name='submit_rating')

]
