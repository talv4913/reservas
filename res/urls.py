from django.urls import path

from .views import StaffView,UsuarioView,DisponibilidadView

urlpatterns = [
    path('propias/', UsuarioView.as_view(), name='reservas_usuario_get'),
    path('propias/<int:pk>/', UsuarioView.as_view(), name='reservas_usuario_delete'),
    path('staff/', StaffView.as_view(), name='reservas_staff_get'),
    path('staff/<int:pk>/', StaffView.as_view(), name='reservas_staff_delete'),
    path('disponibilidad/', DisponibilidadView.as_view(), name='disponibilidad'),
] 