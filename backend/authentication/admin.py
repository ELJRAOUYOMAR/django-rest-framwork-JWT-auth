# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    # readonly_fields = ('jwt_token',)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),  # Remove duplicate "email" field
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("name", "email", "is_staff", "is_logged_in" ,'get_jwt_token')
    search_fields = ("name", "email")
    ordering = ("name",)

    def is_logged_in(self, obj):
        # Use the is_logged_in method defined in the User model
        return obj.is_logged_in()

    is_logged_in.short_description = 'Logged In'
    is_logged_in.boolean = True


    def jwt_token(self, obj):
        return obj.jwt_token

    jwt_token.short_description = 'JWT Token'

admin.site.register(User, UserAdmin)
