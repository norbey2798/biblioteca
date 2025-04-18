from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Vista para el inicio de sesión
def login_view(request):
    if request.user.is_authenticated:
        return redirect("construction")  # Si ya está autenticado, redirige

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("construction")  # Redirige a la página en construcción
        else:
            return render(request, "usuarios/login.html", {"error": "Usuario o contraseña incorrectos"})
    
    return render(request, "usuarios/login.html")

# Vista protegida con login para mostrar "Sitio en Construcción"
@login_required
def construction_view(request):
    return render(request, "usuarios/construction.html")  # <- También corregido aquí

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect("home")  # <- Corrige el redirect (no pongas la ruta del archivo)

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("construction")

    return render(request, "usuarios/register.html")
