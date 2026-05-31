from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegistrarEmpleado, RutLoginForm
from reciclaje.models import Usuario
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_user(request):
    if request.user.is_authenticated:   
        return redirect_by_role(request.user)

    if request.method == "POST":    
        form = RutLoginForm(request, data=request.POST) 
        if form.is_valid(): 
            user = form.get_user()  
            login(request, user)    
            messages.success(request, "Inicio de sesión exitoso")   
            return redirect_by_role(user)
    else:
        form = RutLoginForm()

    return render(request, 'registration/login.html', {'form': form})

def redirect_by_role(user):
    """Auxiliar para redirigir según el rol en la tabla Usuario o si es Staff"""
    if user.is_staff:
        return redirect('vistadm') 
    try:
        perfil = Usuario.objects.get(user=user)
        
        nombre_rol = str(perfil.id_rol).lower() 
        
        if 'bodega' in nombre_rol:
            return redirect('vistabdga')
        elif 'caja' in nombre_rol:
            return redirect('vstacja')
        elif 'vendedor' in nombre_rol:
            return redirect('vstavnde')
            
    except Usuario.DoesNotExist:
        return redirect('home')
        
    return redirect('home')

def logout_user(request):

    logout(request)
    messages.success(request, "Sesion cerrada")
    return redirect('login')

def create_user(request):
    
    if request.method == "POST":
        form = RegistrarEmpleado(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Cuenta creada con exito")
            return redirect('vistadm')
    else:
        form = RegistrarEmpleado()
        
    return render(request, 'registration/singup.html', {'form':form})
    
    