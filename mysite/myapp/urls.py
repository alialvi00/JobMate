from django.urls import path
from . import views

# This is how we configure a URL path to call a function from views class
urlpatterns = [
    path('loginPage/', views.login_page),
    path('signup/', views.signup_page)
]
