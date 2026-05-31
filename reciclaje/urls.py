from django.urls import path
from .views import (base, vstadm, vstabdg, 
                    vstacaja,vstavnd,listar_empleados,
                    detalle_usuario,eliminar_empleado,
                    acualizar_empleado, nueva_compra,adm_home,
                    ver_boleta_vendedor,ver_boleta_caja) 

urlpatterns = [
    path('', base, name='home'),
    path('vstd/', vstadm, name='vistadm'),
    path('admhm/', adm_home, name='adm_home'),
    path('vstb/', vstabdg, name='vistabdga'),
    path('vstc/', vstacaja, name='vstacja'),
    path('vstv/', vstavnd, name='vstavnde'),
    path('lista_empleados/', listar_empleados, name='vistaepds'),
    path('usuario/<int:pk>/', detalle_usuario, name='detalle_empleados'),
    path('usuario/eliminar/<int:pk>/', eliminar_empleado, name='eliminar_empleado'),
    path('usuario/actualizar/<int:pk>/', acualizar_empleado, name='actualizar_empleado'),
    path('vstv/compra/', nueva_compra, name='compra_nueva'),
    path('vendedor/boleta/<int:id_compra>/', ver_boleta_vendedor, name='boleta_vendedor'),
    path('caja/boleta/<int:id_compra>/', ver_boleta_caja, name='boleta_caja'),
]