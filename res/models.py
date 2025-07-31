from django.db import models
from django.conf import settings
# Create your models here.
class BloqueHorario(models.Model):
    horario = models.TimeField(choices=[('18:00','18:00'),('19:00','19:00'),('20:00','20:00'),('21:00','21:00'),('22:00','22:00'),('23:00','23:00'),('00:00','00:00')])
    class Meta:
        ordering = ['horario']

class ReservaModel(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Creador de la reserva")
    nombre = models.CharField(max_length=200,verbose_name='Nombre completo del responsable')
    dni = models.IntegerField(verbose_name="DNI del responsable")
    comensales = models.IntegerField(verbose_name="Numero de comensales")
    fecha = models.DateField()
    horario = models.ManyToManyField(BloqueHorario)
    class Meta:
        ordering = ['fecha']