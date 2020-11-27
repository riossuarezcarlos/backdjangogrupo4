from django.urls import path

from .views import RegistroView, LoginView, PerfilView, DireccionesView, DireccionView, DireccionUsuarioView, LogoutView

urlpatterns = [
    path('registro', RegistroView.as_view(), name='Registro'),   
    path('login', LoginView.as_view(), name='Login'),
    path('logout', LogoutView.as_view(), name='Logout'),
    path('perfil', PerfilView.as_view(), name='Perfil'),
    path('direccion', DireccionesView.as_view(), name='Direccion'),
    path('direccion/<int:dirId>', DireccionView.as_view(), name='Direccion'),
    path('direccionu/<int:usuId>', DireccionUsuarioView.as_view(), name='Direccion'),
]