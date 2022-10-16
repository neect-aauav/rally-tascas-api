from django.urls import path

from . import views

urlpatterns = [
    # admin login
    path('', views.login),
]