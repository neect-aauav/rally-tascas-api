from django.urls import path

from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # admin login page
    path('', views.login),
    # admin login
    path('login', obtain_auth_token),
    # admin register
    path('register', views.register)
]