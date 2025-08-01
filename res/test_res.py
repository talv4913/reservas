import pytest
from datetime import date, timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model

from res.models import ReservaModel,BloqueHorario

@pytest.mark.django_db #Para usar la db
def test_ver_reservas_usuario(client):
    Usuario = get_user_model()
    usuario = Usuario.objects.create_user(dni=1239132, password='test')
    client.force_login(usuario)
    response = client.get('/reservas/propias/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_crear_reserva_usuario(client):
    Usuario = get_user_model()
    usuario = Usuario.objects.create_user(dni=4112312, password='test')
    client.force_login(usuario)
    bloque1 = BloqueHorario.objects.get(horario= '20:00')
    bloque2 = BloqueHorario.objects.get(horario= '21:00')
    data = {"nombre": "Test", "dni": 4112312, "comensales": 2, "fecha": date.today() + timedelta(days=1), "horario":[bloque1.pk, bloque2.pk] }
    response = client.post('/reservas/propias/', data=data)
    assert response.status_code == 201

@pytest.mark.django_db
def test_borrar_reserva_usuario(client):
    Usuario = get_user_model()
    usuario = Usuario.objects.create_user(dni=1231312, password='aaa')
    client.force_login(usuario)
    reserva = ReservaModel.objects.create(usuario=usuario, nombre="Juan Test", dni=12345678, comensales=2, fecha=date.today() + timedelta(days=1))
    reserva.horario.set(BloqueHorario.objects.filter(horario='18:00'))
    response = client.delete((f'/reservas/propias/{reserva.pk}/'))
    assert response.status_code == 204

@pytest.mark.django_db
def test_fecha_mockeada(client):
    Usuario = get_user_model()
    usuario = Usuario.objects.create_user(dni=4112312, password='test')
    client.force_login(usuario)
    bloque1 = BloqueHorario.objects.get(horario= '20:00')  #parte del post
    bloque2 = BloqueHorario.objects.get(horario= '21:00')
    data = {"nombre": "Test", "dni": 4112312, "comensales": 2, "fecha": date.today() - timedelta(days=1), "horario":[bloque1.pk, bloque2.pk] }

    dia_fake = date(2025,1,1)
    with patch('res.serializers.date') as mock_date: # parte del mock
        mock_date.today.return_value = dia_fake
        response = client.post('/reservas/propias/', data=data)
        assert response.status_code == 201

@pytest.mark.django_db
def test_fecha_NO_mockeada(client):
    Usuario = get_user_model()
    usuario = Usuario.objects.create_user(dni=4112312, password='test')
    client.force_login(usuario)
    bloque1 = BloqueHorario.objects.get(horario= '20:00')
    bloque2 = BloqueHorario.objects.get(horario= '21:00')
    data = {"nombre": "Test", "dni": 4112312, "comensales": 2, "fecha": date.today() - timedelta(days=1), "horario":[bloque1.pk, bloque2.pk] }
    response = client.post('/reservas/propias/', data=data)
    assert response.status_code == 400