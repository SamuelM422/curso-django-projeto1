from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe

# Create your views here.
def home(request):
    published_recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, "recipes/pages/home.html", context={
        'recipes': published_recipes
    })

def category(request, category_id):
    # noinspection PyTypeChecker
    published_recipes_by_category = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id, 
            is_published=True)
            .order_by('-id')
    )

    return render(request, "recipes/pages/category.html", context={
        'recipes': published_recipes_by_category,
        'title': published_recipes_by_category[0].category.name # type: ignore
    })

def recipes(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, is_published=True)
    return render(request, "recipes/pages/recipe-view.html", context={
        'recipe': recipe,
        'is_detail_page': True
    })