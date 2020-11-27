from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response

from rest_framework.permissions import  IsAuthenticated

from .models import UsuarioModel, DireccionModel
from .serializers import RegistroSerializer, LoginSerializer, DireccionSerializer, PerfilSerializer, LogoutSerializer

from rest_framework_simplejwt.serializers import TokenObtainSerializer
# Create your views here.

class RegistroView(CreateAPIView):
    queryset = UsuarioModel.objects.all()
    serializer_class = RegistroSerializer
    def post(self, request):
        usuCorreo = request.data.get('usuCorreo')
        usuario = self.get_queryset().filter(usuCorreo = usuCorreo).first()

        if usuario:
            return Response({
                'ok': False,
                'content': None,
                'message': 'Ya se encuentra registrado un usuario con el correo {}'.format(usuCorreo)
            })
        else:
            respuesta = self.get_serializer(data = request.data)
            if respuesta.is_valid(raise_exception=True): 
                resultado = respuesta.create()
                return Response({
                    'ok': True,
                    'content': self.get_serializer(resultado).data,
                    'message': 'Usuario creado exitosamente'
                }, status=200)
            else:
                return Response({
                    'ok': False,
                    'content': None,
                    'message': 'Data incorrecta'
                }, status=400) 

class PerfilView(RetrieveUpdateDestroyAPIView):
    serializer_class = PerfilSerializer
    queryset = UsuarioModel.objects.all()
    permission_classes = (IsAuthenticated, )
 
    def get(self, request):
        usuId = request.user.usuId
        respuesta = self.get_serializer(self.get_queryset().get(usuId=usuId))
        if respuesta :
            return Response({
                'ok': True,
                'content': respuesta.data,
                'message': None

            })

    def put(self, request):
        usuId = request.user.usuId
        respuesta = self.serializer_class(self.get_queryset().get(usuId=usuId), data=request.data)
        
        if respuesta.is_valid(raise_exception=True):
            resultado = respuesta.update()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
            })
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': 'Ocurrió un error en la actualización'
            })


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializador = self.get_serializer(data = request.data)
        serializador.is_valid(raise_exception=True)
        return Response({
            'ok': True,
            'content': serializador.data,
            'message': None
        })

class DireccionesView(ListCreateAPIView):
    queryset = DireccionModel.objects.all()
    serializer_class = DireccionSerializer
    def get(self, request):
        respuesta = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'ok': True,
            'content': respuesta.data,
            'message': None
        })

    def post(self,request):
        respuesta = self.get_serializer(data=request.data)
        if respuesta.is_valid(raise_exception=True):
            respuesta.save()
            return Response({
                'ok': True,
                'content': respuesta.data,
                'message': None
            }, status=201)
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': 'Ocurrió un error al crear la dirección'
            }, status=400)

class DireccionView(RetrieveUpdateDestroyAPIView):
    serializer_class = DireccionSerializer
    queryset = DireccionModel.objects.all()

    def put(self, request, dirId):
        respuesta = self.serializer_class(self.get_queryset().get(dirId=dirId), data=request.data)
        if respuesta.is_valid():
            resultado = respuesta.update()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': None
            })
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': 'Ocurrió un error en la actualización'
            }, status=400)

    def delete(self, request, dirId):
        respuesta = self.get_serializer(self.get_queryset().get(dirId=dirId))
        if respuesta:
            resultado = respuesta.delete()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': 'se deshabilitó la dirección'
            }, status=200)


class DireccionUsuarioView(ListAPIView):
    serializer_class = DireccionSerializer
    queryset = DireccionModel.objects.all()
    def get(self, request, usuId):
        respuesta = self.get_queryset().filter(usuId=usuId).first()
        if respuesta:
            return Response({
                'ok': True,
                'content': self.serializer_class(respuesta).data,
                'message': None
            })


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'ok': True,
            'content': None,
            'message': 'Sesión cerrada correctamente'
        })