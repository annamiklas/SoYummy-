from django.forms import ModelForm

from .models import Ingredient, Recipe, Rating


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ['cook']


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'measurement']


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
