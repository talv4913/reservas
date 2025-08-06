import pytest

from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.

@pytest.mark.django_db
def test_login(client):
    Usuario = get_user_model()
    usuario = Usuario.objects.create_user(dni='1241241', password='hola')

    data = {'dni' : '1241241', 'password' : 'hola'}
    response = client.post('/usuario/token/', data=data)
    assert response.status_code == 200
    assert 'access' in response.json()
    assert 'refresh' in response.json()

@pytest.mark.django_db
def test_register(client):
    data = {'dni' : '1241241', 'password' : 'hola'}
    response = client.post('/usuario/register/', data=data)
    Usuario = get_user_model()
    assert Usuario.objects.filter(dni='1241241').exists()
    assert response.status_code == 201
    usuario =  Usuario.objects.get(dni='1241241')
    assert usuario.check_password('hola')