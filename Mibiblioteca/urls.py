from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("landing.urls")),       #  landing es pagina de inicio
    path("usuarios/", include("usuarios.urls")),  # login  está en /usuarios/
]
