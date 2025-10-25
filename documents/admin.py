from django.contrib import admin
from .models import Entity


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    """
    Admin configuration for Entity model.
    """
    list_display = ("id", "type", "company", "created_at")
    list_filter = ("type", "company")
    search_fields = ("id", "company__name")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at")
