from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
from django.contrib.auth.models import User



class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categoria'

    def __str__(self):
        return self.nombre


class Receta(models.Model):
    titulo = models.CharField(max_length=50)
    subtitulo = models.CharField(max_length=200)
    ingredientes = models.TextField(blank=True)
    pasos = RichTextField()
    tiempo_coccion = models.CharField(max_length=50)
    imagen = models.ImageField(null=True, blank=True, upload_to='img/')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    autor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'receta'

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.imagen:
            self.imagen = 'img/3.jpg'
        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username