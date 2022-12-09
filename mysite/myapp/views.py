from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import CreateUserForm
from django.contrib.auth.models import User

# Create your views here.
# view class takes a request and returns a response (What an HTTP request would do)
# think of view class as a request handler
# action class
from django.views.decorators.csrf import ensure_csrf_cookie


def login_page(request):
    return render(request, 'login-page/login.html')


def signup_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.username = form.cleaned_data.get('username')
            user.profile.email = form.cleaned_data.get('email')
            user.is_active = False
            user.save()
            return redirect('/loginPage')

    context = {'form': form}
    return render(request, 'signup/signup-page.html', context)
