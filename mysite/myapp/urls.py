from django.urls import path
from . import views

# This is how we configure a URL path to call a function from views class
urlpatterns = [
    path('hello/', views.say_hello),
    path('loginPage/', views.show_html),
    path('signup/', views.show_signup_page)
]
