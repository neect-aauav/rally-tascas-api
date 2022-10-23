from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ('name', 'nmec', 'username', 'date_joined', 'last_login', 'is_superuser', 'is_admin', 'is_staff', 'is_active')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)