from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, ReadOnlyPasswordHashField
from reciclaje.models import Usuario, Rol
from django.contrib.auth.forms import UserChangeForm 
from reciclaje.validacion import validar_rut

class RegistrarEmpleado(UserCreationForm):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    correo = forms.EmailField(max_length=254, required=True, label="Correo Electrónico")
    telefono = forms.CharField(max_length=15, required=True, label="Número Telefónico")
    rol = forms.ModelChoiceField(queryset=Rol.objects.all())

    class Meta:
        model = User
        fields = ['username', 'nombre','apellido', 'rol','telefono','correo']
        labels = {'username': 'RUT'}

    def clean_username(self):
        rut = self.cleaned_data['username']

        validar_rut(rut)

        return rut.replace(".", "").upper()
    
    def save(self, commit=True):

        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellido']
        user.email = self.cleaned_data['correo']
        
        if commit:
            user.save()
            Usuario.objects.create(
                user=user,
                rut=self.cleaned_data['username'],
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                id_rol=self.cleaned_data['rol'],
                telefono=self.cleaned_data['telefono'],
                correo=self.cleaned_data['correo'],
            )
        return user


class RutLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = "RUT"
    def clean_username(self):
        rut = self.cleaned_data['username']
    
        validar_rut(rut)
    
        return rut.replace(".", "").upper()


class EditarEmpleadoForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=15, required=True, label="Número Telefónico")
    correo = forms.EmailField(max_length=254, required=True, label="Correo Electrónico")
    rol = forms.ModelChoiceField(queryset=Rol.objects.all())
    
    password = forms.CharField(
        widget=forms.PasswordInput(), 
        required=False, 
        label="Nueva Contraseña",
        help_text="Déjala en blanco si no deseas cambiarla."
    )
    confirmar_password = forms.CharField(
        widget=forms.PasswordInput(), 
        required=False, 
        label="Confirmar Nueva Contraseña"
    )

    class Meta:
        model = User
        fields = ['username', 'nombre', 'apellido', 'telefono', 'correo', 'rol', 'password', 'confirmar_password']
        labels = {'username': 'RUT'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password or confirmar_password:
            if password != confirmar_password:
                raise forms.ValidationError("Las nuevas contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellido']
        user.email = self.cleaned_data['correo']
        nueva_clave = self.cleaned_data.get("password")
        if nueva_clave:
            user.set_password(nueva_clave)
        
        if commit:
            user.save()
            usuario_custom = user.usuario
            usuario_custom.nombre = self.cleaned_data['nombre']
            usuario_custom.apellido = self.cleaned_data['apellido']
            usuario_custom.telefono = self.cleaned_data['telefono']
            usuario_custom.correo = self.cleaned_data['correo']
            usuario_custom.id_rol = self.cleaned_data['rol']
            usuario_custom.save()
            
        return user