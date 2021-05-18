from django.db.models.query import QuerySet
import django_filters
from django.db.models import Q, F
from django_filters import DateFilter, CharFilter

from .models import Recipe
from .lev_sim import levenshtein_distance, Levenshtein


class RecipeFilter(django_filters.FilterSet):
  search = django_filters.CharFilter(method='my_filter')
  class Meta:
    model = Recipe
    fields = ['search', 'category']

  # def my_filter(self, queryset, value):
  #       return Recipe.objects.filter(
  #           Q(name__icontains=value) | Q(description__icontains=value) | Q(ingredients__icontains=value)
  #       )

  def my_filter(self, queryset, name, value):
    # return Recipe.objects.annotate(lev_dist=levenshtein_distance(name, value)).filter(
    #   lev_dist__lte=2
    # )
    recipes = Recipe.objects.all()
    filtred_recipes = []
    for recipe in recipes:
      for word in recipe.name.split():
        if not levenshtein_distance(word, value) > 2:
          filtred_recipes.append(recipe.id)
      for word in recipe.ingredients.split():
        if not levenshtein_distance(word, value) > 2:
          filtred_recipes.append(recipe.id)
    return Recipe.objects.filter(id__in=filtred_recipes)

  