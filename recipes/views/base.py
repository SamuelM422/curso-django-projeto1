from recipes.models import Recipe
from django.views.generic import ListView
import os
from utils.pagination import make_pagination

# Constants
PER_PAGE = int(os.getenv('PER_PAGE', 6))

class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        pagination_range, page_object = make_pagination(self.request, ctx.get('recipes'), PER_PAGE)

        ctx.update({
            'pagination_range': pagination_range,
            'recipes': page_object,
            'title': ctx.get('recipes')[0].category.name if ctx.get('recipes') else 'No recipes',
        })

        return ctx