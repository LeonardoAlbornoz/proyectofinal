from django.db import models

# Create your models here.
class Blog(models.Model):
    titulo = models.CharField(max_length=20)
    texto_corto = models.CharField(max_length=40)
    texto_largo = models.TextField()
    imagen = models.ImageField(upload_to='images/',verbose_name='Imagen', null=True, blank=True)
    autor = models.CharField(max_length=20)
    fecha = models.DateField(auto_now_add=True)

class Chat(models.Model):
    usuario_to = models.CharField(max_length=20)
    usuario_from = models.CharField(max_length=20)
    mensaje = models.CharField(max_length=150)