from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Vista para el inicio de sesión
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("construction")  # Redirige a la página en construcción
        else:
            return render(request, "usuarios/login.html", {"error": "Usuario o contraseña incorrectos"})
    
    return render(request, "usuarios/login.html")  # <- Corregido aquí

# Vista protegida con login para mostrar "Sitio en Construcción"
@login_required
def construction_view(request):
    return render(request, "usuarios/construction.html")  # <- También corregido aquí

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect("login")  # <- Corrige el redirect (no pongas la ruta del archivo)

