from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import login
from myapp.backends import login_backend

# Create your views here.
# view class takes a request and returns a response (What an HTTP request would do)
# think of view class as a request handler
# action class
from django.views.decorators.csrf import ensure_csrf_cookie


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('psw')

        user = login_backend.authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/homePage')
        else:
            messages.info(request, 'Username or Password is incorrect, please try again!')

    return render(request, 'login-page/login.html')


def signup_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.user_name = form.cleaned_data.get('user_name')
            user.email = form.cleaned_data.get('email')
            user.password = form.cleaned_data.get('password1')
            user.password2 = form.cleaned_data.get('password2')
            user.save()

            messages.success(request, 'Account has been successfully created for ' + user.user_name)
            return redirect('/loginPage')

    context = {'form': form}
    return render(request, 'signup/signup-page.html', context)


def redirect_home_page(request):
    return render(request, 'home-page/home-page.html')
