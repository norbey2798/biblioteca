from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("usuarios.urls")),  # Conectar la app 'usuarios' al proyecto
]
