from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Cliente
from .models import Perfil
from django.http import JsonResponse
from django.views.decorators.http import require_GET
#------------------------------------------------------------------------------------------------
# Vista para el inicio de sesión
def login_view(request):
    if request.user.is_authenticated:
        return redirect('gestion_clientes')  # Redirige si ya está autenticado

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirigir al 'next' si está presente, o a la página de clientes
            next_url = request.GET.get('next', 'gestion_clientes')
            return redirect(next_url)
        else:
            return render(request, 'usuarios/login.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'usuarios/login.html')

#------------------------------------------------------------------------------------------------

# Vista protegida con login para mostrar "gestion clientes"
#@login_required
#def gestion_view(request):
#    return render(request, "usuarios/gestion_clientes.html")  

#------------------------------------------------------------------------------------------------

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect("home") 

#------------------------------------------------------------------------------------------------

def register_view(request):
    if request.method == "POST":
        identificacion = request.POST["identificacion"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        fecha_nacimiento = request.POST["fecha_nacimiento"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("register")

        # Usamos el nombre como nombre de usuario (username)
        username = first_name

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre ya está registrado como usuario.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        Perfil.objects.create(
            user=user,
            identificacion=identificacion,
            fecha_nacimiento=fecha_nacimiento
        )

        messages.success(request, "Registro exitoso. Inicia sesión ahora.")
        return redirect("login")

    return render(request, "usuarios/register.html")
'''def register_view(request):
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
        messages.success(request, "Registro exitoso. Inicia sesión ahora.")
        return redirect("login")

    return render(request, "usuarios/register.html")'''

#------------------------------------------------------------------------------------------------

@login_required
def gestion_clientes_view(request):
    if request.method == "POST":
        cliente_id = request.POST.get("cliente_id")

        identificacion = request.POST["identificacion"]
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        fecha_nacimiento = request.POST["fecha_nacimiento"]

        if cliente_id:
            # Modo editar
            cliente = Cliente.objects.get(id=cliente_id)
            cliente.identificacion = identificacion
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.fecha_nacimiento = fecha_nacimiento
            cliente.save()
        else:
            # Modo crear
            Cliente.objects.create(
                identificacion=identificacion,
                nombre=nombre,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento
            )

        return redirect("gestion_clientes")

    clientes = Cliente.objects.all()
    return render(request, "usuarios/gestion_clientes.html", {"clientes": clientes})
#------------------------------------------------------------------------------------------------

@login_required
def editar_cliente_view(request, cliente_id):
    # Obtén el cliente que se desea editar, si no existe, genera un error 404
    cliente = get_object_or_404(Cliente, id=cliente_id)

    # Si el método de la solicitud es POST, se actualiza el cliente
    if request.method == "POST":
        cliente.identificacion = request.POST["identificacion"]
        cliente.nombre = request.POST["nombre"]
        cliente.apellido = request.POST["apellido"]
        cliente.fecha_nacimiento = request.POST["fecha_nacimiento"]
        cliente.save()  # Guarda los cambios en la base de datos

    return redirect("gestion_clientes")  # Redirige a la vista de gestión de clientes

#------------------------------------------------------------------------------------------------

# Vista para eliminar un cliente
def eliminar_cliente_view(request, cliente_id):
    if request.method == 'POST':
        # Buscar al cliente por su ID
        cliente = get_object_or_404(Cliente, id=cliente_id)
        
        try:
            # Eliminar el cliente
            cliente.delete()
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

#------------------------------------------------------------------------------------------------

@login_required
@require_GET
def buscar_cliente_view(request):
    identificacion = request.GET.get('identificacion')
    try:
        cliente = Cliente.objects.get(identificacion=identificacion)
        return JsonResponse({
            "id": cliente.id,
            "identificacion": cliente.identificacion,
            "nombre": cliente.nombre,
            "apellido": cliente.apellido,
            "fecha_nacimiento": str(cliente.fecha_nacimiento)
        })
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

#------------------------------------------------------------------------------------------------

@login_required
def listar_clientes_view(request):
    clientes = Cliente.objects.all()
    data = [{
        "id": c.id,
        "identificacion": c.identificacion,
        "nombre": c.nombre,
        "apellido": c.apellido,
        "fecha_nacimiento": str(c.fecha_nacimiento)
    } for c in clientes]
    return JsonResponse(data, safe=False)