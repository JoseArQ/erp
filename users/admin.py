from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from company.models import Company

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin panel for User model with company and role fields.
    """
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Company info", {"fields": ("company", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "company", "role", "is_staff", "is_superuser"),
        }),
    )

    list_display = ("username", "email", "role", "company", "is_staff", "is_superuser")
    list_filter = ("role", "company", "is_staff", "is_superuser")
    search_fields = ("username", "email")
    ordering = ("username",)

