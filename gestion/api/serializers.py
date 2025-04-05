from django.core.cache import cache
from rest_framework import serializers
from gestion import models as m_gestion



class InformacionPersonasModelSerializer(serializers.ModelSerializer):

    graficas_asociadas = serializers.SerializerMethodField()

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