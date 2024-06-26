from django import forms
from frontend.models import Receta, Categoria
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserChangeForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User
from . import models

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        exclude = ['autor']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitulo': forms.TextInput(attrs={'class': 'form-control'}),
            'ingredientes': forms.Textarea(attrs={'class': 'form-control'}),
            'pasos': forms.CharField(widget=CKEditorWidget()),
            'tiempo_coccion': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': False}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            # 'autor': forms.HiddenInput(),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),

        }

class PerfilForm(UserChangeForm):
    password = None  # Si no deseas que el formulario incluya el campo de contraseña

    class Meta:
        model = User
        fields = ['username', 'first_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Requerido')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')