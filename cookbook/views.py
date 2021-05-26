from django.forms.models import modelformset_factory
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory

from .models import Ingredient, Rating, Recipe
from .forms import RecipeForm, IngredientForm, RatingForm
from .filters import RecipeFilter
from category.models import Category


@login_required
def recipes_page(request, category_slug=None):
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

    context = {
        'page_number': page_number,
        'page_obj': page_obj,
        'myFilter': myFilter,
    }
    return render(request, 'cookbook/recipes.html', context)


@login_required
def edit_recipe_page(request, idR):
    cook = request.user.userprofile
    recipe = Recipe.objects.get(id=idR)
    ingredients = Ingredient.objects.filter(recipe=recipe)
    IngredientFormSet = modelformset_factory(Ingredient, form=IngredientForm)
    formset = IngredientFormSet(queryset=ingredients)
    form = RecipeForm(instance=recipe)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = IngredientFormSet(request.POST or None, queryset=ingredients)
        if form.is_valid():
            form.save()
            if formset.is_valid():
                Ingredient.objects.filter(recipe=recipe).delete()
                for form_ing in formset:
                    if form_ing.is_valid() and form_ing.cleaned_data.get('name'):
                        create_ingredient(form_ing, recipe)
                return redirect('accounts:user_profile')
        else:
            messages.error('Some field is required!')
            formset = IngredientFormSet(queryset=ingredients)

    context = {
        'form': form,
        'recipe': recipe,
        'cook': cook,
        'formset': formset,
    }
    return render(request, 'cookbook/edit_recipe.html', context)


@login_required
def recipe_page(request, idR):
    recipe = Recipe.objects.get(id=idR)
    ingredients = Ingredient.objects.filter(recipe=recipe)
    cook = recipe.cook
    categories = recipe.category.all()
    ingredients_to_string = []

    for ingredient in ingredients:
        ing_str = str(ingredient.quantity)
        if ingredient.quantity and ing_str.split('.')[1] == '0':
            ing_str = ing_str[:-2]
        ingredients_to_string.append(
            f'{ingredient.name} {ing_str if ingredient.quantity else ""}\
                {ingredient.measurement if ingredient.measurement else ""}')

    context = {
        'cook': cook,
        'recipe': recipe,
        'categories': categories,
        'ingredients': ingredients_to_string,
    }

    return render(request, 'cookbook/recipe.html', context)


def create_ingredient(form, recipe):
    cleaned_data = form.cleaned_data
    name = cleaned_data.get('name')
    quantity = cleaned_data.get('quantity')
    measurement = cleaned_data.get('measurement')
    ingredient = Ingredient(recipe=recipe, name=name, quantity=quantity, measurement=measurement)
    ingredient.save()


@login_required
def create_recipe_page(request):
    cook = request.user.userprofile
    recipe = Recipe(cook=cook)
    form = RecipeForm(instance=recipe)
    IngredientFormSet = formset_factory(IngredientForm, extra=2)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = IngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            form.save()
            for form in formset:
                if form.is_valid() and form.cleaned_data.get('name'):
                    create_ingredient(form, recipe)
            return redirect('accounts:user_profile')
    else:
        formset = IngredientFormSet()

    context = {
        'form': form,
        'formset': formset
    }
    return render(request, 'cookbook/create_recipes.html', context)


@login_required
def delete_recipe(request, idR):
    recipe = Recipe.objects.get(id=idR)
    recipe.delete()
    return redirect('accounts:user_profile')


def submit_rating(request, idR):
    recipe = Recipe.objects.filter(id=idR)[0]
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            rating = Rating.objects.get(user__id=request.user.userprofile.id, recipe=recipe)
            form = RatingForm(request.POST, instance=rating)
            form.save()
            return redirect(url)
        except Rating.DoesNotExist:
            form = RatingForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                rating = cleaned_data.get('rating')
                rating = Rating(rating=rating, user=request.user.userprofile, recipe=recipe)
                rating.save()
                return redirect(url)
            else:
                return Http404(form.errors)
