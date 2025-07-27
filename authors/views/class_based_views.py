from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe
from django.http.response import Http404


@method_decorator(login_required(login_url='authors:login', redirect_field_name='next'),
                  name='dispatch')
class DashboardRecipe(View):
    def get_recipe(self, pk):
        recipe = None

        if pk is not None:
            recipe = Recipe.objects.filter(author=self.request.user, is_published=False, pk=pk)

            if not recipe:
                raise Http404()

        return recipe

    def render_recipe(self, form):

        return render(self.request, 'authors/pages/dashboard_recipe.html',
                      context={'form': form})

    def get(self, request, pk=None):
        recipe = self.get_recipe(pk)

        form = AuthorRecipeForm(
            instance=recipe[0] if recipe else None
        )

        return self.render_recipe(form)

    def post(self, request, pk=None):
        recipe = self.get_recipe(pk)

        form = AuthorRecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe[0] if recipe else None
        )

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, 'Recipe updated successfully')

            return redirect(reverse('authors:dashboard_recipe_edit', kwargs={'pk': recipe.id}))

        return self.render_recipe(form)

@method_decorator(login_required(login_url='authors:login', redirect_field_name='next'),
                  name='dispatch')
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))

        recipe.delete()
        messages.success(self.request, 'Recipe deleted successfully')

        return redirect('authors:dashboard')