from django import forms
from .models import Proveedor
from .validacion import validar_rut

class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedor
        fields = ['rut', 'nombre', 'apellido', 'telefono', 'email']
        
        # LOS WIDGETS DEBEN IR AQUÍ ADENTRO DE LA CLASE META
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control form-control-lg text-uppercase', 
                'placeholder': '12345678-K',
                'id': 'id_rut'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: Juan'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: Pérez'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '912345678',
                'type': 'tel'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'juan.perez@email.com'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['rut'].required = True
        self.fields['nombre'].required = True
        self.fields['apellido'].required = True

    def clean_rut(self):
        rut = self.cleaned_data.get("rut")

        if rut:
            validar_rut(rut)
            rut = rut.replace(".", "").replace("-", "").upper()
            return rut

        return rut