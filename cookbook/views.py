from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .models import Recipe
from .forms import RecipeForm

# Create your views here.

def recipesPage(request):
  recipes = Recipe.objects.all().order_by('-data_created')
  # print("TYPE",type(Recipe.objects.all()))
  # print("TYPE",type([1, 3, 4]))

  # myFilter = RecipeFilter(request.GET, queryset=recipes)
  # recipes = myFilter.qs

  paginator = Paginator(recipes, 6)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  # fav_list = request.user.cook.like_recipe.all()
  # print(fav_list)

  context = {
    'page_number' : page_number,
    'page_obj' : page_obj,
    # 'myFilter' : myFilter,
    # 'fav_list': fav_list,

  }
  return render(request, 'cookbook/recipes.html', context)


def editRecipePage(request, idR):
  cook = request.user.userprofile
  recipe = Recipe.objects.get(id=idR)
  form = RecipeForm(instance=recipe)
  if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        print('POST')
        if form.is_valid():
            print('valid')
            form.save()
            return redirect('accounts:user_profile')
        print(form.errors)
  context = {
    'form': form, 
    'recipe': recipe,
    'cook': cook
  }
  return render(request, 'cookbook/edit_recipe.html', context)


def recipePage(request, id):
  recipe = Recipe.objects.get(id=id)
  cook = recipe.cook
  categories = recipe.category.all()
  context = {
    'cook': cook,
    'recipe': recipe,
    'categories': categories
  }
  return render(request, 'cookbook/recipe.html', context)

def createRecipePage(request):
  cook = request.user.userprofile
  recipeIns = Recipe(cook=cook)
  form = RecipeForm(instance=recipeIns)
  if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipeIns)
        if form.is_valid():
            form.save()
            return redirect('accounts:user_profile')
  context = {
    'form': form, 
  }
  return render(request, 'cookbook/create_recipes.html', context)


def deleteRecipe(request, idR):
  recipe = Recipe.objects.get(id=idR)
  recipe.delete()
  return redirect('accounts:user_profile')