from django.db.models import query
from django.forms.formsets import BaseFormSet
from django.contrib import messages
from django.forms.models import modelform_factory, modelformset_factory
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory

from .models import Ingredient, Rating, Recipe
from .forms import RecipeForm, IngridientForm, RatingForm
from .filters import RecipeFilter
from category.models import Category

# Create your views here.
@login_required
def recipesPage(request, category_slug=None):
  recipes = None
  if category_slug:
    category = get_object_or_404(Category, slug=category_slug)
    recipes = Recipe.objects.filter(category=category)
  else:
    recipes = Recipe.objects.all().order_by('-creation_date')

  myFilter = RecipeFilter(request.GET, queryset=recipes)
  recipes = myFilter.qs

  paginator = Paginator(recipes, 6)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  # fav_list = request.user.cook.like_recipe.all()
  # print(fav_list)

  context = {
    'page_number' : page_number,
    'page_obj' : page_obj,
    'myFilter' : myFilter,
    # 'fav_list': fav_list,

  }
  return render(request, 'cookbook/recipes.html', context)


# @login_required
# def editRecipePage(request, idR):
#   cook = request.user.userprofile
#   recipe = Recipe.objects.get(id=idR)
#   ingredients = Ingredient.objects.filter(recipe=recipe)
#   IngridientFormSet = inlineformset_factory(Recipe, Ingredient, extra=2, fields=('name','amount','unit'))
#   formset = IngridientFormSet(instance=recipe)
#   form = RecipeForm(instance=recipe)
#   if request.method == 'POST':
#         form = RecipeForm(request.POST, request.FILES, instance=recipe)
#         formset = IngridientFormSet(request.POST or None, instance=recipe)
#         if formset.is_valid() and form.is_valid():
#             formset.save()
#             form.save()
#             return redirect('accounts:user_profile')
#         else:
#           print(formset.non_form_errors())
#           formset = IngridientFormSet(instance=recipe)
#   context = {
#     'form': form, 
#     'recipe': recipe,
#     'cook': cook,
#     'formset': formset,
#   }
#  return render(request, 'cookbook/edit_recipe.html', context)


@login_required
def editRecipePage(request, idR):
  cook = request.user.userprofile
  recipe = Recipe.objects.get(id=idR)
  ingredients = Ingredient.objects.filter(recipe=recipe)
  number_of_ingredients = len(ingredients)
  IngridientFormSet = modelformset_factory(Ingredient, form=IngridientForm)
  formset = IngridientFormSet(queryset=ingredients)
  # formset = IngridientFormSet(instance=recipe)
  form = RecipeForm(instance=recipe)
  if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = IngridientFormSet(request.POST or None, queryset=ingredients)
        if formset.is_valid() and form.is_valid():
            formset.save()
            form.save()
            return redirect('accounts:user_profile')
        else:
          print(formset.non_form_errors())
          print(formset.errors)
          formset = IngridientFormSet(queryset=ingredients)
          # raise ValidationError()
  context = {
    'form': form, 
    'recipe': recipe,
    'cook': cook,
    'formset': formset,
  }
  return render(request, 'cookbook/edit_recipe.html', context)

@login_required
def recipePage(request, id):
  recipe = Recipe.objects.get(id=id)
  ingredients = Ingredient.objects.filter(recipe=recipe)
  cook = recipe.cook
  categories = recipe.category.all()
  context = {
    'cook': cook,
    'recipe': recipe,
    'categories': categories,
    'ingredients': ingredients,
  }
  return render(request, 'cookbook/recipe.html', context)


@login_required
def createRecipePage(request):
  cook = request.user.userprofile
  recipe_ins = Recipe(cook=cook)
  form = RecipeForm(instance=recipe_ins)
  IngredientFormSet = formset_factory(IngridientForm, extra=2)
  if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe_ins)
        formset = IngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            form.save()
            for form in formset:
              if form.is_valid():
                cleaned_data = form.cleaned_data
                name = cleaned_data.get('name')
                amount = cleaned_data.get('amount')
                unit = cleaned_data.get('unit')
                ingridient = Ingredient(recipe=recipe_ins, name=name, amount=amount, unit=unit)
                ingridient.save()
            return redirect('accounts:user_profile')
  else:
    formset = IngredientFormSet()

  context = {
    'form': form,
    'formset': formset 
  }
  return render(request, 'cookbook/create_recipes.html', context)


@login_required
def deleteRecipe(request, idR):
  recipe = Recipe.objects.get(id=idR)
  recipe.delete()
  return redirect('accounts:user_profile')




def submitRate(request, id):
    recipe = Recipe.objects.filter(id=id)[0]
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            rate = Rating.objects.get(user__id=request.user.userprofile.id, recipe=recipe)
            form = RatingForm(request.POST, instance=rate)
            form.save()
            return redirect(url)
        except Rating.DoesNotExist:
            print('jdjdjdd')
            form = RatingForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                rating = cleaned_data.get('rating')
                rate = Rating(rating=rating, user=request.user.userprofile, recipe=recipe)
                rate.save()
                return redirect(url)
            else: 
              print(form.errors)