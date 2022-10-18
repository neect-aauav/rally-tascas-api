from django.urls import path

from . import views

urlpatterns = [
    # admin login
    path('', views.login),
    # admin register
    path('register', views.register)
]