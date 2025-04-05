from django.contrib import admin
from gestion import models as model_gestion

# Register your models here.
@admin.register(model_gestion.Persona)
class PersonaModelAdmin(admin.ModelAdmin):
    pass

@admin.register(model_gestion.RecursosInstucion)
class RecursosInstucion(admin.ModelAdmin):
    pass

@admin.register(model_gestion.Instuciones)
class Instuciones(admin.ModelAdmin):
    pass

@admin.register(model_gestion.Municipios)
class Municipios(admin.ModelAdmin):
    pass

@admin.register(model_gestion.Departamento)
class Departamento(admin.ModelAdmin):
    pass

@admin.register(model_gestion.Pais)
class Pais(admin.ModelAdmin):
    pass


@admin.register(model_gestion.TipoDocumento)
class TipoDocumento(admin.ModelAdmin):
    pass


@admin.register(model_gestion.Ubicacion)
class Ubicacion(admin.ModelAdmin):
    pass