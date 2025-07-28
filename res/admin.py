from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario
# Register your models here.
class UsuarioAdmin(UserAdmin):
    list_display = ('dni', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff','is_superuser','is_active')
    search_fields = ('dni',)