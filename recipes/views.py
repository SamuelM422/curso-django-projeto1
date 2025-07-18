from django.shortcuts import render
from recipes.models import Recipe
from utils.recipes.factory import make_recipe

# Create your views here.
def home(request):
    recipes = Recipe.objects.all().order_by('-id')
    return render(request, "recipes/pages/home.html", context={
        'recipes': recipes
    })

def category(request, category_id):
    recipes = Recipe.objects.filter(category__id=category_id).order_by('-id')
    return render(request, "recipes/pages/home.html", context={
        'recipes': recipes,
        'is_detail_page': True
    })

def recipes(request, recipe_id):
    recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipes/pages/recipe-view.html", context={
        'recipe': recipe,
        'is_detail_page': True
    })