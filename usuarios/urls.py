from django.urls import path

from .views import login_view, logout_view, register_view, gestion_clientes_view, editar_cliente_view, eliminar_cliente_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("gestion_clientes/", gestion_clientes_view, name="gestion_clientes"),#para crear
    path("gestion_clientes/<int:cliente_id>/", editar_cliente_view, name="editar_cliente"),  # Editar cliente
    path('eliminar_cliente/<int:cliente_id>/', eliminar_cliente_view, name='eliminar_cliente'), #Eliminar cliente 
]

