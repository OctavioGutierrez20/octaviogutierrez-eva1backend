from django.contrib import admin
from .models import Contact

admin.site.register(Contact)
class contactAdmin(admin.ModelAdmin):
    list_display = ("nombre","precio","stock","activo")
    search_fields = ("nombre",)
    list_filter = ("activo",)
    ordering = ("nombre", "stock",)

admin.site.register(model_or_iterable=Contact, admin_class=contactAdmin)


