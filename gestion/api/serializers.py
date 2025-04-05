from django.core.cache import cache
from rest_framework import serializers
from gestion import models as m_gestion



class InformacionPersonasModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = m_gestion.Persona
        fields = [
            "id",
            "Nombre",
            "Apellido",
            "TipoId",
            "NroId",
            "Telefono",
            "sexo"
        ]

class InformacionInstitucionesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = m_gestion.Instuciones
        fields = [
            "id",
            "CodInstucion",
            "descripcion",
            "ciudad",
            "Departamento"
        ]