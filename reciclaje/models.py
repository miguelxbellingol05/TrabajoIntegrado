from django.db import models
from django.contrib.auth.models import User
from .validacion import validar_rut

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_rol

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    
    id_rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    telefono = models.CharField(max_length=15, null=True, blank=True, verbose_name="Número Telefónico")
    correo = models.EmailField(max_length=254, null=True, blank=True, verbose_name="Correo Electrónico")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def clean_rut(self):
        rut = self.cleaned_data["rut"]

        validar_rut(rut)

        return rut.replace(".", "").upper()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.id_rol}"
    

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    def clean_rut(self):
        rut = self.cleaned_data["rut"]

        validar_rut(rut)

        return rut.replace(".", "").upper()
    class Meta:
        db_table = 'PROVEEDOR'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return f"{self.rut} - {self.nombre} {self.apellido}"

class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)

    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, db_column='id_proveedor')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='id_usuario')
    
    fecha_hora = models.DateTimeField(auto_now_add=True)
    numero_acta_pdi = models.CharField(max_length=50, null=True, blank=True)
    total_pagado = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    forma_pago = models.CharField(max_length=50, default='Efectivo')
    estado = models.CharField(max_length=30, default='Emitido')

    foto_evidencia = models.ImageField(upload_to='evidencias/', null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'COMPRA'

    def __str__(self):
        return f"Compra #{self.id_compra} - {self.id_proveedor.nombre}"

class TipoMetal(models.Model):
    id_metal = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    precio_actual = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'TIPO_METAL'

    def __str__(self):
        return self.nombre
    
class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    id_metal = models.ForeignKey(TipoMetal, on_delete=models.PROTECT, db_column='id_metal')
    stock_actual_kg = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    id_usuario_responsable = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column='id_usuario_responsable',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'INVENTARIO'

    def __str__(self):
        return f"{self.id_metal.nombre} - {self.stock_actual_kg}"


class DetalleCompra(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_compra = models.ForeignKey(Compra, on_delete=models.CASCADE, db_column='id_compra')
    metal_nombre = models.CharField(max_length=100) 
    peso_kg = models.DecimalField(max_digits=10, decimal_places=3)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'DETALLE_COMPRA'