from rest_framework import routers, viewsets    

from .models import Contact

from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ProductoSerializer

router = routers.DefaultRouter()
router.register(r'Contact', ProductoViewSet)