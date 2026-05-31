from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['rut', 'nombre', 'apellido', 'telefono', 'email']
        
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

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        return rut

    def clean(self):
        cleaned_data = super().clean()

        if 'rut' in self._errors:
            del self._errors['rut']
        return cleaned_data