from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
from django.urls.exceptions import Http404  # type: ignore
from django.db.models import Q
from utils.pagination import make_pagination
import os

# Constants
PER_PAGE = int(os.getenv('PER_PAGE', 6))

# Create your views here.
def home(request):
    published_recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    pagination_range, page_object = make_pagination(request, published_recipes, PER_PAGE)

    return render(request, "recipes/pages/home.html", context={
        'recipes': page_object,
        'pagination_range': pagination_range
    })

def category(request, category_id):
    # noinspection PyTypeChecker
    published_recipes_by_category = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id, 
            is_published=True)
            .order_by('-id')
    )

    pagination_range, page_object = make_pagination(request, published_recipes_by_category, PER_PAGE)

    return render(request, "recipes/pages/category.html", context={
        'recipes': page_object,
        'pagination_range': pagination_range,
        'title': published_recipes_by_category[0].category.name # type: ignore
    })

def recipes(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, is_published=True)
    return render(request, "recipes/pages/recipe-view.html", context={
        'recipe': recipe,
        'is_detail_page': True
    })

def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    search_filtered_recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term,)
        ) &
        Q(is_published=True),
    ).order_by('-id')

    pagination_range, page_object = make_pagination(request, search_filtered_recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html',
                  context={'search_term': search_term,
                           'page_title': f'Search results for: "{search_term}"',
                           'recipes': page_object,
                           'pagination_range': pagination_range,
                           'additional_url_query': '&q=' + search_term,
                           })