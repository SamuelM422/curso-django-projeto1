from django.shortcuts import render, redirect
from authors.forms import RegisterForm
from django.http import Http404 # type: ignore
from django.contrib import messages

# Create your views here.
def register_view(request):
    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html',
                  context={'form': form}
                  )

def register_create(request):
    if not request.POST:
        raise Http404()

    request.session['register_form_data'] = request.POST
    form = RegisterForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'Account created successfully')

        del(request.session['register_form_data'])
        
    return redirect('authors:register')