from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="AdminUsuario",
        default_version="V1",
        description="App para gestionar usuarios y acceso",
        terms_of_service="https://www.google.com",
        contact=openapi.Contact(email="riossuarezcarlos@gmail.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('admin/', admin.site.urls),
    path('API/', include('user.urls')),
]
