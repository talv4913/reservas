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

class BloqueHorario(models.Model):
    horario = models.TimeField(choices=[('18:00','18:00'),('19:00','19:00'),('20:00','20:00'),('21:00','21:00'),('22:00','22:00'),('23:00','23:00'),('00:00','00:00')])
    class Meta:
        ordering = ['horario']

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Creador de la reserva")
    nombre = models.CharField(max_length=200,verbose_name='Nombre completo del responsable')
    dni = models.IntegerField(verbose_name="DNI del responsable")
    comensales = models.IntegerField(verbose_name="Numero de comensales")
    fecha = models.DateField() #fechas futuras no mas de 2 meses antelacion
    horario = models.ManyToManyField(BloqueHorario)
    class Meta:
        ordering = ['fecha']