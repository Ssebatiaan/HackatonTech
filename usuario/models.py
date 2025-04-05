from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from usuario.managers import MyUserManager
from django.core import validators
import re
from .choices import TIPO_USUARIO



class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=200, null=True, choices=TIPO_USUARIO, verbose_name="nombre")
    descripcion = models.TextField(null=True, blank=True, verbose_name="descripcion")

    def __str__(self) -> str:
        return self.nombre if self.nombre else ""

    class Meta:
        verbose_name = 'Tipo de usuario'
        verbose_name_plural = 'Tipos de usuarios'


class Usuario(AbstractBaseUser, PermissionsMixin):
    correo = models.EmailField(_('Correo'),
                               max_length=255,
                               unique=True, )
    cedula = models.CharField(max_length=30, unique=True, null=True, validators=[
        validators.RegexValidator(re.compile("^[1-9][0-9]{6,30}$"), ('No valida'), 'invalid')])
    celular = models.CharField(max_length=40, null=True, validators=[
        validators.RegexValidator(re.compile("^[1-9][0-9]{5,30}$"), ('No valida'), 'invalid')])
    contacto = models.CharField(max_length=200, null=True)
    descripcion = models.TextField(null=True)
    is_staff = models.BooleanField(default=False)
    nombre_usuario = models.CharField(max_length=100, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=datetime.now)
    ultima_conexicon = models.DateTimeField(auto_now_add=True)
    nacimiento = models.DateField(_('Cumpleaños'), blank=True, null=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50, blank=True, null=True)
    ocupacion = models.CharField(max_length=50, blank=True, null=True)
    foto = models.ImageField(upload_to='foto_perfil/', blank=True, null=True)
    USERNAME_FIELD = 'correo'
    direccion = models.CharField(max_length=30, null=True)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="tipo de usuario")
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    @property
    def full_name(self):
        return '{} {}'.format(self.nombre or '', self.apellidos or '')

    def __str__(self):
        return self.correo

    def __unicode__(self):
        return '{} {} / {}'.format(self.nombre, self.apellidos, self.correo)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['nombre', "apellidos"]
