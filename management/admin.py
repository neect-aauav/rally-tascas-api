from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import Members, Teams

from .models import Account, DBLogger

class AccountAdmin(UserAdmin):
    list_display = ('name', 'nmec', 'username', 'bar', 'date_joined', 'last_login', 'is_superuser', 'is_admin', 'is_staff', 'is_active')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class DBLoggerAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'type', 'status', 'message')
    readonly_fields = ('user', 'time', 'type', 'status', 'message')
    search_fields = ['user', 'type', 'status']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class TeamsAdmin(admin.ModelAdmin):
    list_display = ('name','points', 'drinks', 'has_egg', 'puked', 'phone', 'best_name', 'best_team_costume', 'won_special_game')
    readonly_fields = ('qr_code', 'created')
    search_fields = ['name']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class MembersAdmin(admin.ModelAdmin):
    list_display = ('name', 'points', 'drinks', 'team')
    search_fields = ['name']
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(DBLogger, DBLoggerAdmin)
admin.site.register(Teams, TeamsAdmin)
admin.site.register(Members, MembersAdmin)
