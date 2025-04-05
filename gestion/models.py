from django.db import models

# Create your models here.
class Persona(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    DOCUMENTOS_CHOICES = [
        ('TI', 'Tarjeta de Identidad'),
        ('CC', 'Cedula de Ciudadania'),
        ('P', 'Pasaporte'),
    ]
    Nombre = models.CharField(max_length=200)
    Apellido = models.CharField(max_length=200)
    TipoId = models.CharField(max_length=20, choices=DOCUMENTOS_CHOICES)
    NroId = models.IntegerField(max_length=200)
    Telefono = models.IntegerField(max_length=200)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

class RecursosInstucion(models.Model):
    NomRecurso = models.CharField(max_length=200)
    Cantidad = models.IntegerField(max_length=200)
    
class Instuciones(models.Model):
    CodInstucion = models.IntegerField(max_length=200)
    descripcion = models.TextField(max_length=800)
    ciudad = models.CharField(max_length=200)
    Departamento = models.CharField(max_length=200)

class Municipios(models.Model):
    Desc = models.CharField(max_length=200)
    
class Departamento(models.Model):
    Desc = models.CharField(max_length=200)
    
class Pais(models.Model):
    Desc = models.CharField(max_length=200)

class TipoDocumento(models.Model):
    Desc = models.CharField(max_length=200)
    
class Ubicacion(models.Model):
    Barrio = models.CharField(max_length=200)
    Direccion = models.TextField(max_length=800)
    Municipio = models.ForeignKey(Municipios, on_delete=models.CASCADE)
    Departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    Pais = models.ForeignKey(Pais, on_delete=models.CASCADE)