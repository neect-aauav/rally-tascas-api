from django.urls import path

from . import views

urlpatterns = [
    # signup
    path('signup', views.signup),
]