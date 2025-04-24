from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Cliente(models.Model):
    identificacion = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

#----------------------------------------------------------------------------------------------

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identificacion = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
        