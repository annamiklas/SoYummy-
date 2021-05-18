from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'cookbook'

urlpatterns = [
    path('recipes/', views.recipesPage, name='recipes'),
    path('recipes/<slug:category_slug>/', views.recipesPage, name='recipe_category'),
    path('edit_recipe/<str:idR>', views.editRecipePage, name="edit_recipe"),
    path('recipe/<str:id>', views.recipePage, name="recipe"),
    path('delete_recipe/<str:idR>', views.deleteRecipe, name="delete_recipe"),
    path('create_recipe/', views.createRecipePage, name="create_recipe"),
    path('submit_rate/<str:id>', views.submitRate, name='submit_rate')

]
