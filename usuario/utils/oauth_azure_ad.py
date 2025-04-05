import jwt
import requests
import json
from rest_framework.response import Response
from rest_framework import status
from usuario.api import serializers as serializer_usuario
from usuario import models as model_usuario
from rest_framework.authtoken.models import Token
from rest_framework_jwt.settings import api_settings
import random
import string



def generate_auth_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


def generate_password():
    characters = string.ascii_letters + string.digits
    password = "".join(random.choice(characters) for x in range(10))
    return password


def validacion_token_azure_ad(id_token=None, tenant="common"):
    try:
        """
        It takes an id_token and a tenant, and returns a dictionary with the user's name, email, and tenant
        
        :param id_token: The JWT token that you want to validate
        :param tenant: The Azure AD tenant (directory) that the user is from. For work or school accounts,
        this is the domain of the user's email address. For personal Microsoft accounts, this is "live.com",
        defaults to common (optional)
        """
        #el tenant es el id de inquilino de la aplicacion, cuando se valide autenticacion solo
        #con usuarios de la plataforma
        client_id = '1f829f37-fc96-4f56-8a83-0c9d4a345d77'

        # Obtener el certificado de firma de Azure AD
        url = f'https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys'
        response = requests.get(url)
        keys = response.json()['keys']

        # Verificar la firma del ID token
        header = jwt.get_unverified_header(id_token)

        kid = header['kid']

        key = None
        for k in keys:
            if k['kid'] == kid:
                key = k
                break
        if key:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
            try:
                payload = jwt.decode(id_token, public_key, audience=client_id, algorithms='RS256')
            except jwt.ExpiredSignatureError:
                return Response({"error":"el token ha expirado"}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.InvalidTokenError:
                return Response({"error":"token invalido"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                correo_usuario = payload.get("email",None)
                nombre_usuario = payload.get("name",None)
                if not correo_usuario:
                    return Response({"error":"token invalido, no contiene informacion de correo de usuario"}, status=status.HTTP_400_BAD_REQUEST)
                if not nombre_usuario:
                    return Response({"error":"token invalido, con contiene informacion de nombre de usuario"}, status=status.HTTP_400_BAD_REQUEST)
                status_usuario = False
                usuario = model_usuario.Usuario.objects.filter(
                    correo = correo_usuario.lower(),
                    is_staff = True
                ).first()
                if not usuario:
                    usuario = model_usuario.Usuario(
                        correo = correo_usuario.lower(),
                        is_staff = True
                    )
                    usuario.save()
                else:
                    status_usuario = True
                if usuario.password is None:
                    password_generada = generate_password()
                    usuario.set_password(password_generada)
                usuario.nombre = nombre_usuario
                usuario.save()
                if usuario.tipo_usuario:
                    response_data = serializer_usuario.UserSerializer(usuario,many=False).data
                    refresh_token = Token.objects.filter(user=usuario)
                    if refresh_token.exists():
                        refresh_token.delete()
                    refresh_token = Token.objects.create(user=usuario)
                    token = generate_auth_token(usuario)
                    response_data.update({**{
                                        'token':token,
                                        'refresh_token': refresh_token.key,
                                        'offline': False,
                                        'tipo_usuario':{
                                            "id":usuario.tipo_usuario.id if usuario.tipo_usuario else None,
                                            "nombre":usuario.tipo_usuario.nombre if usuario.tipo_usuario else None
                                        }
                                        }})
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    if status_usuario:
                        return Response({
                                "ok":"usuario registrado con exito, debe solicitar a \
                                los administradores que le asocien un rol para que pueda ingresar al sistema"
                            }, 
                            status=status.HTTP_201_CREATED
                            )
                    else:
                        return Response({
                                "error":"no puede ingresar hasta que un administrador le asigne un rol"
                            }, 
                            status=status.HTTP_401_UNAUTHORIZED
                            )
        else:
            return Response({"error":"token invalido"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"error":"error interno, contacte al administrador"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)