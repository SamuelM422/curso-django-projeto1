from django.http import Http404
from recipes.models import Recipe
from recipes.views.base import RecipeListViewBase
from django.views.generic import DetailView
from django.db.models import Q
from django.http import JsonResponse

from tag.models import Tag


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

class RecipeListViewApi(RecipeListViewBase):
    def render_to_response(self, context, **response_kwargs):
        recipes_qs = self.get_queryset()
        data = list(recipes_qs.values())

        return JsonResponse(data, safe=False, **response_kwargs)


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

class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()

        qs = qs.filter(
            tags__slug=self.kwargs.get('slug', ''),
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(slug=self.kwargs.get('slug', '')).first()

        if not page_title:
            page_title = 'No recipes found'

        ctx.update({
            'page_title': f'{page_title} - Tag',
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

class RecipeDetailApi(RecipeDetailView):
    def render_to_response(self, context, **response_kwargs):
        recipes_qs = self.get_queryset()
        data = list(recipes_qs.values())

        return JsonResponse(
            data,
            safe=False
        )