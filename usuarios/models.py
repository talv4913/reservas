from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class UsuarioManager(BaseUserManager):
    def create_user(self, dni, password=None, **extra):
        if not dni:
            raise ValueError("El DNI es obligatorio")
        usuario = self.model(dni=dni, **extra)
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self,dni, password, **extra):
        if not dni:
            raise ValueError("El DNI es obligatorio")
        if not password:
            raise ValueError("La contrasenia es obligatoria")
        usuario = self.model(dni=dni, is_staff=True, is_superuser=True, **extra)
        usuario.set_password(password)
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):
    dni = models.IntegerField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = UsuarioManager()
    USERNAME_FIELD = 'dni'

    def __str__(self):
        return str(self.dni)
