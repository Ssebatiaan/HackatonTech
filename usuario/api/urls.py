from django.urls import path, re_path, include
from django.conf.urls import url
from rest_framework_jwt.views import verify_jwt_token
from rest_framework.routers import DefaultRouter
from usuario.api.viewsets import ObtainJSONWebTokenCustom, CustomRefreshJSONWebToken, ServiceValidationAPI, \
    ObtainJSONWebTokenCustomOffice365, LogoutJSONWebToken
from rest_framework.authtoken.views import obtain_auth_token
from . import viewsets as vs


router = DefaultRouter()
router.register(r'tipo_usuario', vs.TipoUsuarioModelViewSet)
router.register(r'usuario', vs.UsuarioModelViewSet)


#Authenticate
urlpatterns = [
    url(r'^', include(router.urls)),
    path('autenticacion_office365/', ObtainJSONWebTokenCustomOffice365.as_view(), name='authenticar'), #OK
    path('autenticar/', ObtainJSONWebTokenCustom.as_view(), name='authenticar'), #OK
    path('autorizar/', obtain_auth_token, name='autorizar'), #OK
    path("logout/", LogoutJSONWebToken.as_view(), name="logout"),
    path('refresh/', CustomRefreshJSONWebToken.as_view(), name='refresh-token'), #OK
    path('validar/', verify_jwt_token, name='validate-token'), #OK
    path('services_validation/', ServiceValidationAPI.as_view(), name='hello_word'), #OK
]