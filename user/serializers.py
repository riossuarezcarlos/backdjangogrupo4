from rest_framework import serializers
from django.contrib import auth
from .models import UsuarioModel, DireccionModel
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = UsuarioModel
        fields = ['usuCorreo', 'password', 'is_superuser', 'is_staff']

    def create(self): 
        is_superuser = self.validated_data.get('is_superuser')
        is_staff = self.validated_data.get('is_staff')
        usuCorreo = self.validated_data.get('usuCorreo')
        password = self.validated_data.get('password')
        nuevoUsuario = UsuarioModel(is_superuser = is_superuser, is_staff = is_staff, usuCorreo = usuCorreo)
        nuevoUsuario.set_password(password)
        nuevoUsuario.save()
        return nuevoUsuario

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioModel
        exclude = ['last_login', 'usuCorreo', 'password', 'is_staff', 'is_active', 'is_superuser', 'date_joined', 'groups', 'user_permissions']
 
    def update(self):
        self.instance.usuNombre = self.validated_data.get('usuNombre', self.instance.usuNombre)
        self.instance.usuApellido = self.validated_data.get('usuApellido', self.instance.usuApellido)
        self.instance.usuDni = self.validated_data.get('usuDni', self.instance.usuDni)
        self.instance.usuCel = self.validated_data.get('usuCel', self.instance.usuCel)
        self.instance.save()
        return self.instance


class LoginSerializer(serializers.ModelSerializer):
    usuCorreo = serializers.EmailField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=50, min_length=6, write_only=True)
    class Meta:
        model = UsuarioModel
        fields = ['usuCorreo', 'password', 'tokens']

    def validate(self, attrs):
        usuCorreo = attrs.get('usuCorreo', '')
        password = attrs.get('password', '')

        usuario = auth.authenticate(usuCorreo = usuCorreo, password = password)
        if not usuario:
            raise AuthenticationFailed('Credenciales invalidas, intentelo de nuevo')
        return{
            'uid': usuario.usuId,
            'usuCorreo': usuario.usuCorreo,
            'tokens': usuario.tokens
        }


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DireccionModel
        exclude = ['estado']

    def update(self):
        self.instance.dirDes = self.validated_data.get('dirDes', self.instance.dirDes)
        self.instance.dirNum = self.validated_data.get('dirNum', self.instance.dirNum)
        self.instance.dirPer = self.validated_data.get('dirPer', self.instance.dirPer)
        self.instance.dirRef = self.validated_data.get('dirRef', self.instance.dirRef)
        self.instance.usuId = self.validated_data.get('usuId', self.instance.usuId)
        self.instance.save()
        return self.instance

    def delete(self):
        self.instance.estado = False
        self.instance.save()
        return self.instance

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': {'Token is expired or invalid'}
    }

    def validate(self, attr):
        self.token = attr['refresh']
        return attr

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            self.fail('bad_token')

