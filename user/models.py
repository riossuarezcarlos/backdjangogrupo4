from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

# Sobrescribir clases usuario

class ManejoUsuario(BaseUserManager):
    use_in_migrations=True
    def _create_user(self, usuCorreo, usuNombre, usuPass, **extra_fields):
        values= [usuCorreo, usuNombre]
        fields_value_map = dict(zip(self.model_REQUIRED_FIELDS, values))
        for field_name, value in fields_value_map.items():
            if not value:
                raise ValueError("EL valor de {} debe estar definido".format(field_name))
        usuCorreo = self.normalize_email(usuCorreo)
        user = self.model(
            usuCorreo = usuCorreo,
            usuNombre = usuNombre,
            **extra_fields
        )
        user.set_password(usuPass)
        user.save(using=self._db)
        return user

    def create_user(self, usuCorreo, usuNombre, usuPass=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(usuCorreo, usuNombre, usuPass, **extra_fields)

    def create_superuser(self, usuCorreo, usuNombre, usuPass=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El super usuario debe de ser staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El super usuario debe de ser superusuario')
        return self._create_user( usuCorreo, usuNombre, usuPass, **extra_fields)

# Create your models here.

class UsuarioModel(AbstractBaseUser, PermissionsMixin):
    usuId = models.AutoField(db_column='usu_id', primary_key=True)
    usuCorreo = models.EmailField(db_column='usu_correo', unique=True)
    usuNombre = models.CharField(db_column='usu_nombre', null=True, max_length=50)
    usuApellido = models.CharField(db_column='usu_apellido', default='', max_length=50)
    usuDni = models.CharField(db_column='usu_dni', default='', max_length=50)
    usuCel = models.CharField(db_column='usu_cel', default='', max_length=13)
    password = models.TextField(db_column='usu_pass')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default = timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = ManejoUsuario()

    USERNAME_FIELD = 'usuCorreo'
    # REQUIRED_FIELDS = ['usuNombre', 'usuApellido', 'usuDni']

    def tokens(self):
        tokens = RefreshToken.for_user(self)
        return{
            'acceso': str(tokens.access_token),
            'refresh': str(tokens)
        }

    class Meta:
        db_table = 't_usuario'


# Model Direccion

class DireccionModel(models.Model):
    dirId = models.AutoField(db_column='dir_id', primary_key=True, null=False, unique=True)
    dirDes = models.CharField(db_column='dir_des', max_length=200)
    dirNum = models.CharField(db_column='dir_num', max_length=10)
    dirPer = models.CharField(db_column='dir_per', max_length=50)
    dirRef = models.CharField(db_column='dir_ref', max_length=100)
    usuId = models.ForeignKey(UsuarioModel, on_delete = models.PROTECT, db_column='usu_id', related_name='DireccionUsuario')
    estado = models.BooleanField(db_column='estado',null=False, default=True)

    createAt = models.DateTimeField(db_column='created_at', auto_now_add=True)
    updateAt = models.DateTimeField(db_column='updated_at', auto_now=True)    
    class Meta:
        db_table = 't_direccion'
 