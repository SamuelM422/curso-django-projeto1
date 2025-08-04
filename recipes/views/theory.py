from django.shortcuts import render
from recipes.models import Recipe

def theory(request, *args, **kwargs):
    recipes = Recipe.objects.all()

    context={
        'recipes': recipes,
    }

    return render(
        request,
        'recipes/pages/theory.html',
        context=context,
    )