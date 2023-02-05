from django.urls import path
from . import views

# This is how we configure a URL path to call a function from views class
urlpatterns = [
    path('loginPage/', views.login_page),
    path('signup/', views.signup_page),
    path('homePage/', views.redirect_home_page),
    path('resume-upload/', views.resume_upload, name='resume_upload'),
    path('job-search/', views.find_job, name='job-search'),
    path('rate-resume/', views.rate_resume, name='rate-resume')
]
