from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
# view class takes a request and returns a response (What an HTTP request would do)
# think of view class as a request handler
# action class

def say_hello(request):
    return HttpResponse('Hello World')


def show_html(request):
    return render(request, 'login-page/login.html')
