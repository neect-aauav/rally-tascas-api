from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from management import views as management_views 
from rallytascas import views as rallytascas_views

schema_view = get_schema_view(
    openapi.Info(
        title="NEECT Rally Tascas",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # swagger docs
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # admin /register
    path('register', management_views.register),
    # admin /login
    path('login', obtain_auth_token),
    # admin /token
    path('token', management_views.check_token),
    # admin /admin/<token>
    path('admin/<slug:token>', management_views.admin),

    # /teams
    path('teams', views.teams),
    # /teams/<id>
    path('teams/<slug:id>', views.teams),
    # /members
    path('members', views.members),
    # /members/<id>
    path('members/<slug:id>', views.members),
    # /bars
    path('bars', views.bars),
    # /bars/<id>
    path('bars/<slug:id>', views.bars),
    # /points/<id>
    path('points/<slug:id>', views.points),
    # /points/<id>/<{add, remove}>
    path('points/<slug:id>/<slug:method>', views.points),
    # /qrcodes/<id>
    path('qrcodes/<slug:id>', views.qrcodes),
    # /games
    path('games', views.games),
    # /games/<id>
    path('games/<slug:id>', views.games),
    # /prizes
    path('prizes', views.prizes),
    # /prizes/<id>
    path('prizes/<slug:id>', views.prizes),
    
    # /teamplay
    path('teamplay', rallytascas_views.teamplay),

    # /scoreboard/teams
    path('scoreboard/teams', rallytascas_views.scoreboard_teams),
    # /scoreboard/members
    path('scoreboard/members', rallytascas_views.scoreboard_members),
    # /scoreboard/members/<team>
    path('scoreboard/members/<slug:team>', rallytascas_views.scoreboard_members),
]