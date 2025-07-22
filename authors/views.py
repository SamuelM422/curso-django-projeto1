from django.shortcuts import render, redirect
from authors.forms.register_form import RegisterForm
from authors.forms.login_form import LoginForm
from django.http import Http404 # type: ignore
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login

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
        
    return redirect('authors:register')

def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html',
                  context={
                      'form': form,
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
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    else:
        messages.error(request, 'Invalid username or password.')
    return redirect('authors:login')