from django.contrib import admin
from .models import Contact

class contactAdmin(admin.ModelAdmin):
    list_display = ("name","phone","email","address")
    search_fields = ("name",)
    list_filter = ("phone",)
    ordering = ("name", "address",)

admin.site.register(model_or_iterable=Contact, admin_class=contactAdmin)
