from django.contrib import admin
from .models import Rol, Usuario, Proveedor, Compra, DetalleCompra, TipoMetal


admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Proveedor)
admin.site.register(TipoMetal)
admin.site.register(Compra)
admin.site.register(DetalleCompra)