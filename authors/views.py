from django.shortcuts import render, redirect
from django.http import Http404 # type: ignore
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from authors.forms.register_form import RegisterForm
from authors.forms.login_form import LoginForm
from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe

# Create your views here.
def register_view(request):
    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html',
                  context={'form': form,
                           'form_action': reverse('authors:register_create')}
                  )

def register_create(request):
    if not request.POST:
        raise Http404()

    request.session['register_form_data'] = request.POST
    form = RegisterForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Account created successfully')

        del(request.session['register_form_data'])
        return redirect('authors:login')
        
    return redirect('authors:register')

def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html',
                  context={
                      'form': form,
                      'form_action': reverse('authors:login_create')
                  })

def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'You have been logged in successfully')
            login(request, authenticated_user)
            return redirect('authors:dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    else:
        messages.error(request, 'Invalid username or password.')
    return redirect('authors:login')

@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request.')
        return redirect('authors:login')

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user.')
        return redirect('authors:login')

    messages.success(request, 'You have been logged out successfully.')
    logout(request)
    return redirect('authors:login')

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_view(request):
    recipes = Recipe.objects.filter(author=request.user, is_published=False)
    return render(request, 'authors/pages/dashboard.html',
                  context={'recipes': recipes})

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe(request, pk):
    recipe = Recipe.objects.filter(author=request.user, is_published=False, pk=pk)

    if not recipe:
        raise Http404()

    form = AuthorRecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe[0]
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Recipe updated successfully')

        return redirect(reverse('authors:dashboard_recipe_edit', kwargs={'pk': pk}))

    return render(request, 'authors/pages/dashboard_recipe.html',
                  context={'form': form})