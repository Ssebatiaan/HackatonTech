from django.contrib.auth.models import User
from django.db.models import Q
from datetime import date
from usuario import models as m_usuario
from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_jwt.serializers import VerificationBaseSerializer
from datetime import datetime, timedelta
from calendar import timegm
from django.utils.translation import ugettext_lazy as _
from usuario.models import Usuario
from usuario import models as m_usuario



expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA
jwt_playload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_playload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER



class UserSerializer(ModelSerializer):

    class Meta:
        model = Usuario
        fields = ['pk',
                  'cedula',
                  'nombre',
                  'contacto',
                  'correo',
                  'direccion',
        ]

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        keys =[key for key, value in data.items() if value is None]
        data.update({key:'' for key in keys})
        return data


class CustomRefreshJSONWebTokenSerializer(VerificationBaseSerializer):
    """
    Refresh an access token.
    TODO: The test test_refresh_token_view_will_send_new_refresh_token_if_jwt_token_time_has_expired shows that we
    have a security issue. This should be refactor to not allow invalid token to refresh them.
    """

    def validate(self, attrs):
        try:
            token = attrs['token']

            payload = self._check_payload(token=token)
            user = self._check_user(payload=payload)
            # Get and check 'orig_iat'
            orig_iat = payload.get('orig_iat')

            if orig_iat:
                # Verify expiration
                refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA
                if isinstance(refresh_limit, timedelta):
                    refresh_limit = (refresh_limit.days * 24 * 3600 +
                                     refresh_limit.seconds)

                expiration_timestamp = orig_iat + int(refresh_limit)
                now_timestamp = timegm(datetime.utcnow().utctimetuple())

                if now_timestamp > expiration_timestamp:
                    msg = _('Refresh has expired.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('orig_iat field is required.')
                raise serializers.ValidationError(msg)

            new_payload = jwt_payload_handler(user)
            new_payload['orig_iat'] = orig_iat

            return {
                'token': jwt_encode_handler(new_payload),
                'user': user
            }
        except ValidationError as exc:
            if "Signature has expired." in exc.detail:
                if self.context.get('request').data.get('refresh_token', None):
                    refresh_token = self.context.get('request').data.get('refresh_token')
                    token = Token.objects.filter(key=refresh_token)

                    if token.exists():
                        token = token.first()
                        user = User.objects.get(pk=token.user.id)

                        # Delete and recreate a new token for refresh next time (unvalidated old token)

                        token.delete()
                        new_refresh_token = Token.objects.create(user=user)

                        payload = jwt_payload_handler(user)

                        return {
                            'token': jwt_encode_handler(payload),
                            'user': user,
                            'refresh_token': new_refresh_token
                        }

            raise exc  # If not refresh token, raise again exception raised by DRF JWT library


class TipoUsuarioModelSerializer(serializers.ModelSerializer):

    value = serializers.CharField(source='id', read_only=True)
    label = serializers.CharField(source='nombre', read_only=True)

    class Meta:
        model = m_usuario.TipoUsuario
        fields = [
            "value",
            "label",
        ]
        extra_kwargs = {
            'value': {'read_only': True},
        }


class UsuarioModelSerializer(serializers.ModelSerializer):

    #tipo_usuario = TipoUsuarioModelSerializer(required=False, many=False)

    class Meta:
        model = m_usuario.Usuario
        fields = [
            "id",
            "nombre",
            "apellidos",
            "correo",
            "tipo_usuario",
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            "correo": {'read_only': True},
            "tipo_usuario": {'required': False},
            "nombre": {'required': False},
        }
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance


class UsuarioListModelSerializer(serializers.ModelSerializer):

    tipo_usuario = serializers.SerializerMethodField()

    class Meta:
        model = m_usuario.Usuario
        fields = [
            "id",
            "nombre",
            "apellidos",
            "correo",
            "tipo_usuario",
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            "correo": {'read_only': True},
            "tipo_usuario": {'required': False},
            "nombre": {'required': False},
        }

    def get_tipo_usuario(self, obj):
        return obj.tipo_usuario.nombre if obj.tipo_usuario else "no tiene grupo asociado"