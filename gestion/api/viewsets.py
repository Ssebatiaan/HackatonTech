from datetime import datetime
from rest_framework import filters, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from gestion import models as m_gestion
from . import serializers as serializers_gestion
from .sqls import graficas
import json
from .utils import utils_viewsets
from django.http import HttpResponse
from openpyxl import Workbook
import os


    
class PersonasDashboardModelViewSet(viewsets.ModelViewSet):
    queryset = m_gestion.Persona.objects.all()
    serializer_class = serializers_gestion.InformacionPersonasModelSerializer
    
    @action(methods=['GET'], detail=True)
    def obtener_informacion_personas(self, request, pk=None):
        #categoria_dashboard =  self.get_queryset().filter(rol_asociado__id=request.user.tipo_usuario.id, categoria_asociada__id = pk)
        informacion_personas =  self.get_queryset()
        if informacion_personas:
            data = serializers_gestion.InformacionPersonasModelSerializer(informacion_personas, many=True).data
            #input(data)
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error":"no hay personas registradas en el aplicativo, contacte con el administrador para mas informacion"}, status=status.HTTP_400_BAD_REQUEST)
    
class InstitucionesDashboardModelViewSet(viewsets.ModelViewSet):
    queryset = m_gestion.Instuciones.objects.all()
    serializer_class = serializers_gestion.InformacionInstitucionesModelSerializer
    
    @action(methods=['GET'], detail=True)
    def obtener_informacion_Instituciones(self, request, pk=None):
        #categoria_dashboard =  self.get_queryset().filter(rol_asociado__id=request.user.tipo_usuario.id, categoria_asociada__id = pk)
        informacion_Instituciones =  self.get_queryset()
        if informacion_Instituciones:
            data = serializers_gestion.InformacionInstitucionesModelSerializer(informacion_Instituciones, many=True).data
            #input(data)
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error":"no hay instituciones registradas en el aplicativo, contacte con el administrador para mas informacion"}, status=status.HTTP_400_BAD_REQUEST)
    
     