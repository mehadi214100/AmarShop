from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

admin.site.site_header = "Amar Shop"
admin.site.site_title = "Amar Shop"
admin.site.index_title = "Welcome to Your Admin Panel"

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'city', 'phone')
    list_filter = ('is_active','city')
    fieldsets = (
            (None, {'fields': ('email', 'password')}),
            ('Personal Info', {'fields': ('first_name', 'last_name', 'city', 'phone')}),
            ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser', 'is_active')}),
    )
    search_fields = ('email', 'first_name')
    filter_horizontal = ()
    ordering = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(userProfile)