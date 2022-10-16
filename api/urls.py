from django.urls import path

from . import views

urlpatterns = [
    # /teams
    path('teams', views.teams),
    # /teams/<id>
    path('teams/<slug:id>', views.teams),
	# /missions/missionId/
    #path('<slug:value>', views.missions),
]