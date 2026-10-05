from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "email",
        "address",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "email")
    list_filter = ("created_at", "updated_at")
    ordering = ("name", "email")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Informacion del contacto",
            {"fields": ("name", "phone", "email", "address")},
        ),
        (
            "Metadatos",
            {"fields": ("created_at", "updated_at")},
        ),
    )
