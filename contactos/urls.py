from django.urls import path

from .views import ContactCreateView, ContactDeleteView, ContactListView, ContactUpdateView

from .models import Contact
from rest_framework import routers, serializers, viewsets

class productoSerializer(serializers.ModelSerializer):
    class meta:
        model = Contact
        fields = '_all_'

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializers_class = productoSerializer

router = routers.DefaultRouter()
router.register(r'Contact', ProductViewSet)
    
app_name = "contactos"

urlpatterns = [
    path("lista", ContactListView.as_view(), name="list"),
    path("nuevo/", ContactCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", ContactUpdateView.as_view(), name="update"),
    path("<int:pk>/eliminar/", ContactDeleteView.as_view(), name="delete"),
]