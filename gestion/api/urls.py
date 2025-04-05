from django.conf.urls import url
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import viewsets as vs


router = DefaultRouter()
router.register(r'personas', vs.PersonasDashboardModelViewSet)
#router.register(r'filtro_grafica', vs.FiltroGraficaModelViewSet)
#router.register(r'opcion_filtro_grafica', vs.OpcionFiltroGraficaModelViewSet)
#router.register(r'categoria_grafica', vs.CategoriaGraficaModelViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]