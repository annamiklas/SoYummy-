from django.contrib.auth import models
from accounts.models import UserProfile
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Ingredient, Recipe, Rating


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ['cook']

class IngridientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'
        exclude = ['recipe']        

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']

