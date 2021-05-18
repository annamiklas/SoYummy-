from django import forms
from django.contrib import admin

from .models import Ingredient, Rating, Recipe

# Register your models here.

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Rating)