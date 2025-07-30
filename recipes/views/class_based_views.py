from django.http import Http404
from recipes.models import Recipe
from recipes.views.base import RecipeListViewBase
from django.views.generic import DetailView
from django.db.models import Q


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(category__id=self.kwargs.get('category_id'),
                       is_published=True,)

        if not qs:
            raise Http404()

        return qs

class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self):
        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404()

        qs = super().get_queryset()

        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term,)
            ) &
            Q(is_published=True),
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        ctx.update({
            'search_term': search_term,
            'page_title': f'Search results for: "{search_term}"',
            'additional_url_query': '&q=' + search_term,
        })

        return ctx

class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True, pk=self.kwargs.get('pk'))

        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'is_detail_page': True,
        })

        return ctx