from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import TipoMetal, Compra, Usuario, Inventario
from .models import Usuario
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from registration.forms import EditarEmpleadoForm
from .forms import ProveedorForm
from .models import Proveedor, Compra, DetalleCompra, Usuario, TipoMetal, Inventario
from decimal import Decimal
import json

# Create your views here.
def base(request):
    return render(request, 'reciclaje/base.html')


#-----ADMINISTRADOR-------
@staff_member_required
def adm_home(request):
    return render(request, 'reciclaje/admin/adm_home.html')

@staff_member_required
def vstadm(request):

    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('home')

    return render(request, 'reciclaje/vistadm.html')

@staff_member_required
def listar_empleados(request):
    
    usuarios = Usuario.objects.all()
    return render(request, 'reciclaje/admin/lista_empleados.html', {'listado': usuarios})

@staff_member_required
def detalle_usuario(request, pk):
    
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'reciclaje/admin/detalle_empleados.html', {'usuario': usuario})

@staff_member_required
def eliminar_empleado(request, pk):
   
    empleado = get_object_or_404(Usuario, pk=pk)
    
    user_nativo = empleado.user     
    if user_nativo:
            user_nativo.delete()
    else:
            empleado.delete()
    messages.success(request, 'Empleado eliminado correctamente.')    
    return redirect('vistaepds')

@staff_member_required
def acualizar_empleado(request, pk):
    empleado = get_object_or_404(Usuario, pk=pk)
    user_instance = empleado.user 
    
    form = EditarEmpleadoForm(
        request.POST or None, 
        instance=user_instance,
        initial={
            'nombre': empleado.nombre,
            'apellido': empleado.apellido,
            'telefono': empleado.telefono,
            'correo': empleado.correo,
            'rol': empleado.id_rol
        }
    )
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Empleado {empleado.nombre} actualizado correctamente.') 
        return redirect('detalle_empleados', pk=empleado.pk)
        
    return render(request, 'reciclaje/admin/actualizar_empleado.html', {
        'form': form, 
        'usuario': empleado
    })

#-----/ADMINISTRADOR-------

def vstabdg(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    inventarios = Inventario.objects.select_related(
        'id_metal',
        'id_usuario_responsable'
    ).all()

    return render(request, 'reciclaje/vistabdga.html', {'inventarios' : inventarios})

def vstavnd(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'reciclaje/vendedor/home_vndedor.html') 

#-----CAJA-------
@login_required
def vstacaja(request):
    if request.method == 'POST':
        pass
    compras = Compra.objects.all().order_by('-fecha_hora')
    
    return render(request, 'reciclaje/vistacaja.html', {'compras': compras})

@login_required
def ver_boleta_caja(request, id_compra):
    compra = get_object_or_404(Compra, pk=id_compra)
    detalles = DetalleCompra.objects.filter(id_compra=compra)
    return render(request, 'reciclaje/caja/boleta.html', {'compra': compra, 'detalles': detalles})
#-----/CAJA-------

#-----VENTA-------
@login_required
def nueva_compra(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        
        if form.is_valid():
            rut_prov = form.cleaned_data.get('rut')
            proveedor_instancia, created = Proveedor.objects.get_or_create(
                rut=rut_prov,
                defaults={
                    'nombre': form.cleaned_data.get('nombre'),
                    'apellido': form.cleaned_data.get('apellido'),
                    'telefono': form.cleaned_data.get('telefono'),
                    'email': form.cleaned_data.get('email'),
                }
            )

            try:
                usuario_vendedor = Usuario.objects.get(user=request.user)
            except Usuario.DoesNotExist:
                messages.error(request, "Error: Tu cuenta de usuario no está en la tabla USUARIO.")
                return redirect('vstavnde')

            observaciones_texto = request.POST.get('observaciones')
            metales_json = request.POST.get('lista_metales_json')
            foto_subida = request.FILES.get('foto_metal')

            total_boleta = 0.00

            nueva_compra_obj = Compra.objects.create(
                id_proveedor=proveedor_instancia,
                id_usuario=usuario_vendedor,
                observaciones=observaciones_texto,
                foto_evidencia=foto_subida,
                total_pagado=total_boleta,
                estado='Emitido'
            )

            if metales_json:
                try:
                    lista_metales = json.loads(metales_json)
                    for item in lista_metales:
                        peso = float(item.get('peso', 0))
                        
                        DetalleCompra.objects.create(
                            id_compra=nueva_compra_obj,
                            metal_nombre=item.get('metal'),
                            peso_kg=peso,
                            precio_unitario=0.00,
                            subtotal=0.00
                        )
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error procesando JSON de metales: {e}")

            messages.success(request, "¡Compra guardada con éxito en el servidor!")

            return redirect('ver_boleta', id_compra=nueva_compra_obj.id_compra)
        
        else:
            print(" ERRORES DEL FORMULARIO:", form.errors.as_data())
            messages.error(request, "Por favor revisa los datos del proveedor ingresados.")
            
    else:
        form = ProveedorForm()
        
    return render(request, 'reciclaje/vendedor/neva_compra.html', {'form': form})

@login_required
def ver_boleta_vendedor(request, id_compra):
    compra = get_object_or_404(Compra, pk=id_compra)
    detalles = DetalleCompra.objects.filter(id_compra=compra)
    return render(request, 'reciclaje/vendedor/boleta_vendedor.html', {'compra': compra, 'detalles': detalles})
#-----/VENTA-------
