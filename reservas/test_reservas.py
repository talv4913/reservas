import pytest

from django.contrib.auth import get_user_model

@pytest.mark.django_db #Para usar la db
def test_ver_reservas_usuario(client):
    Usuario = get_user_model()
    usuario = Usuario.objects.create_user(dni=1239132, password='test')
    client.force_login(usuario)
    response = client.get('/reservas/propias/')
    assert response.status_code == 200