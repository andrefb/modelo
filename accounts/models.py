from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# 1. O Manager (O "Gerente" que sabe criar usuários sem username)
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O Email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# 2. O Modelo de Usuário (A Tabela no Banco)
class CustomUser(AbstractUser):
    username = None  # Removemos o campo username
    email = models.EmailField('Endereço de Email', unique=True)
    
    # Campos novos
    name = models.CharField('Nome Completo', max_length=255)
    phone = models.CharField('Telefone', max_length=20, blank=True)

    # Configurações do Django
    USERNAME_FIELD = 'email'  # O login será pelo email
    REQUIRED_FIELDS = ['name', 'phone']  # Campos obrigatórios no terminal (createsuperuser)

    objects = CustomUserManager()

    def __str__(self):
        return self.email