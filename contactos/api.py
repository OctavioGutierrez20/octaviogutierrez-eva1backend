from rest_framework import routers, viewsets    

from .models import Contact

from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ProductoSerializer

routers = routers.DefaultRouter()
routers.register(r'Contact', ProductoViewSet)