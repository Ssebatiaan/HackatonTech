from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from usuario.forms import UsuarioCreationForm, UsuarioChangeForm
from . import models as m_usuario



@admin.register(m_usuario.TipoUsuario)
class TipoUsuarioModelAdmin(admin.ModelAdmin):
    pass


@admin.register(m_usuario.Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    model = m_usuario.Usuario
    list_display = ('correo', 'is_staff', 'is_active',)
    list_filter = ('correo', 'is_active',)
    fieldsets = (
        (None, {'fields': ('nombre','apellidos','cedula','direccion','correo','tipo_usuario','nacimiento','ocupacion', 'password', 'foto')}),
        ('Tipo', {'fields': ('is_staff', 'is_active','is_superuser')}),
        ('Permisos', {'fields': ('user_permissions', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre','apellidos','cedula','direccion','correo','tipo_usuario','nacimiento','ocupacion', 'password1', 'password2', 'foto', 'is_staff', 'is_active')}
         ),
        ('Tipo', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Permisos', {'fields': ('user_permissions', 'groups')}),
    )
    search_fields = ('correo',)
    ordering = ('correo',)
