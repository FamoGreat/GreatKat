from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ('Account', {'fields': ('email', 'username', 'first_name', 'last_name', 'phone_number', 'password')}),
    ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superadmin', 'is_active')}),
    ('Important Dates', {'fields': ('date_joined', 'last_login')})


admin.site.register(Account, AccountAdmin)

