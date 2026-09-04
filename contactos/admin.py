from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "updated_at")
    search_fields = ("name", "email")
    ordering = ("name",)