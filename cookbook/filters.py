import django_filters

from .models import Ingredient, Recipe
from .lev_sim import levenshtein_distance


class RecipeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='my_filter')

    class Meta:
        model = Recipe
        fields = ['search', 'category']


    def my_filter(self, queryset, name, value):
        recipes = Recipe.objects.all()
        filtered_recipes = []
        for recipe in recipes:
            for word in recipe.name.split():
                if not levenshtein_distance(word, value) > 2:
                    filtered_recipes.append(recipe.id)
            ingredients = Ingredient.objects.filter(recipe=recipe)
            for word in ingredients:
                if not levenshtein_distance(word.name, value) > 2:
                    filtered_recipes.append(recipe.id)
        return Recipe.objects.filter(id__in=filtered_recipes)