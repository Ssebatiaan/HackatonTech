from django.contrib.auth import get_user_model
from rest_framework.decorators import permission_classes, action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken, JSONWebTokenAPIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import viewsets
from django.contrib.auth.hashers import check_password
from dashboard_udec.drfconfig.paginations import CFEAPIPagination, StandardResultsSetPagination
from usuario.api.serializers import CustomRefreshJSONWebTokenSerializer, UserSerializer, \
    TipoUsuarioModelSerializer, UsuarioModelSerializer, UsuarioListModelSerializer
from dashboard_udec.drfconfig import permissions as permission_api
from rest_framework.authtoken.models import Token
from rest_framework_jwt.settings import api_settings
from usuario.api.mixins.request_aplication_mixin import RequestAplicationMixin
from usuario.models import Usuario
from rest_framework_jwt.utils import jwt_decode_handler, jwt_payload_handler, jwt_encode_handler
import os
from django.db import connection
from usuario import models as m_usuario
from usuario.utils.oauth_azure_ad import validacion_token_azure_ad



expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA
jwt_playload_handler = api_settings.JWT_PAYLOAD_HANDLER
#jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_playload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
#jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class ObtainJSONWebTokenCustom(ObtainJSONWebToken, RequestAplicationMixin):
    authentication_classes = []
    permission_classes = [permission_api.AnonPermissionOnly]
    user_serializer_class = UserSerializer

    def get_serializer_context(self):
        context = super(ObtainJSONWebTokenCustom, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def post(self, request, *args, **kwargs):
        response = super(ObtainJSONWebTokenCustom, self).post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = get_user_model().objects.get(correo=request.data[get_user_model().USERNAME_FIELD])
            if not user.tipo_usuario:
                return Response({"error":"No tienes un rol asignado, habla con un administrador para que te ayude"}, status=status.HTTP_401_UNAUTHORIZED)
            refresh_token = Token.objects.filter(user=user)
            if refresh_token.exists():
                refresh_token.delete()
            refresh_token = Token.objects.create(user=user)
            serialized_user = self.user_serializer_class(user, context={'request': request})
            response.data.update(serialized_user.data)
            #tipo = self.obtain_user_type()
            response.data.update({**{'refresh_token': refresh_token.key,
                                     'tipo_usuario':{
                                        "id":user.tipo_usuario.id if user.tipo_usuario else None,
                                        "nombre":user.tipo_usuario.nombre if user.tipo_usuario else None
                                     }
                                     }})
            return response
        else:
            return Response({"error":"Problema con las credenciales ingresadas"}, status=status.HTTP_400_BAD_REQUEST)
        

class ObtainJSONWebTokenCustomOffice365(ObtainJSONWebToken, RequestAplicationMixin):
    authentication_classes = []
    permission_classes = [permission_api.AnonPermissionOnly]
    user_serializer_class = UserSerializer

    def get_serializer_context(self):
        context = super(ObtainJSONWebTokenCustom, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get(self, request, *args, **kwargs):
        response = super(ObtainJSONWebTokenCustom, self).post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = get_user_model().objects.get(correo=request.data[get_user_model().USERNAME_FIELD])
            refresh_token = Token.objects.filter(user=user)
            if refresh_token.exists():
                refresh_token.delete()
            refresh_token = Token.objects.create(user=user)
            serialized_user = self.user_serializer_class(user, context={'request': request})
            response.data.update(serialized_user.data)
            tipo = self.obtain_user_type()
            response.data.update({**{'refresh_token': refresh_token.key,
                                     'offline': False,
                                     }, **tipo})
        return response


class CustomRefreshJSONWebToken(JSONWebTokenAPIView):
    serializer_class = CustomRefreshJSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        # Intercept response to add refresh token
        response = super(CustomRefreshJSONWebToken, self).post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            payload = jwt_decode_handler(response.data.get('token'))
            user = get_user_model().objects.get(pk=payload.get('user_id'))
            token = Token.objects.get(user=user)
            response.data.update({'refresh_token': token.key})

        return response

    
class ServiceValidationAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        response_services = {
            "databaseConnection":None,
            "emailConnection":None
        }

        #Email validation
        response_email_server = os.system("ping -c 1 smtp.gmail.com")
        if response_email_server == 0:
            response_services["emailConnection"] = "Ok"

        #Database validation
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            response_database_server = cursor.fetchone()
            if response_database_server:
                response_services["databaseConnection"] = "Ok"
        except Exception as e:
            response_services["databaseConnection"] = "Error: {error}".format(error = str(e))

        return Response(response_services)


class TipoUsuarioModelViewSet(viewsets.ModelViewSet):

    queryset = m_usuario.TipoUsuario.objects.all()
    serializer_class = TipoUsuarioModelSerializer


class UsuarioModelViewSet(viewsets.ModelViewSet):

    queryset = m_usuario.Usuario.objects.all()
    serializer_class = UsuarioModelSerializer

    #@permission_classes([IsAuthenticated])
    def list(self, request, *args, **kwargs):
        queryset = m_usuario.Usuario.objects.all()
        serializer = UsuarioListModelSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def autenticacion_office365(self, request, pk=None):
        usuario = request.user
        #input(request.data)
        #input(usuario.correo)
        #task_reporte.enviar_reporte_email(id_usuario=usuario.id)
        #print("Hola mundo")
        #task_reporte.enviar_reporte_email.apply_async(kwargs={'id_usuario':usuario.id}, countdown=10)
        return Response({"ok":"En un momento se le enviara un correo con el reporte en excel"}, status=status.HTTP_200_OK)
        #return Response({"error":"grafica con id: "+str(pk)+" esta grafica no se encuentra"}, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutJSONWebToken(JSONWebTokenAPIView):
    serializer_class = CustomRefreshJSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        # Intercept response to add refresh token
        response = super(CustomRefreshJSONWebToken, self).post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            payload = jwt_decode_handler(response.data.get('token'))
            user = get_user_model().objects.get(pk=payload.get('user_id'))
            token = Token.objects.get(user=user)
            token.delete()
            response.data.update({'refresh_token': token.key})

        return response