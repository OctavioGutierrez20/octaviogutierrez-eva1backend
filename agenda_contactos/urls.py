from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from contactos.api import router  


def health(request):
    return JsonResponse({"status": "ok", "service": "agenda-clara-backend"})


urlpatterns = [
    path("", health),
    path("health/", health),
    path("admin/", admin.site.urls),
    path("", include("contactos.urls")),
    path("api-auth/", include("rest_framework.urls")),

    path("api/", include(router.urls)),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
