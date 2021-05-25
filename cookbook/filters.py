import django_filters

from .models import Ingredient, Recipe
from .lev_sim import levenshtein_distance


class RecipeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='my_filter')

    class Meta:
        model = Recipe
        fields = ['search']


    def my_filter(self, queryset, name, value):
        filtered_recipes = []

        for query in queryset:
            for word in query.name.split():
                if not levenshtein_distance(word, value) > 2:
                    filtered_recipes.append(query.id)
            ingredients = Ingredient.objects.filter(recipe=query)
            for word in ingredients:
                if not levenshtein_distance(word.name, value) > 2:
                    filtered_recipes.append(query.id)
        return Recipe.objects.filter(id__in=filtered_recipes)