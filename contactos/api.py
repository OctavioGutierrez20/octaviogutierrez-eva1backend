from rest_framework import routers, viewsets

from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


router = routers.DefaultRouter()
router.register(r"contacts", ContactViewSet)