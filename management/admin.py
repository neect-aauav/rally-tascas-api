from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

import management

from .models import Account, DBLogger

class AccountAdmin(UserAdmin):
    list_display = ('name', 'nmec', 'username', 'date_joined', 'last_login', 'is_superuser', 'is_admin', 'is_staff', 'is_active')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class DBLoggerAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'message')
    readonly_fields = ('user', 'time', 'message')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(DBLogger, DBLoggerAdmin)