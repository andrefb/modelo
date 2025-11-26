from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class ActiveCompanyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Company(models.Model):
    STATE_CHOICES = [
        ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'),
        ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'),
        ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'),
        ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'),
        ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
        ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'),
        ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    legal_name = models.CharField('Razão Social', max_length=255)
    cnpj = models.CharField('CNPJ', max_length=20, unique=True)
    
    trade_name = models.CharField('Nome Fantasia', max_length=255, blank=True)
    state_registration = models.CharField('Inscrição Estadual', max_length=20, blank=True)

    phone = models.CharField('Telefone', max_length=20, blank=True)
    phone_2 = models.CharField('Celular/Outro', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)
    website = models.URLField('Site', blank=True)
    
    zip_code = models.CharField('CEP', max_length=10, blank=True)
    address = models.CharField('Logradouro', max_length=255, blank=True)
    number = models.CharField('Número', max_length=20, blank=True)
    complement = models.CharField('Complemento', max_length=100, blank=True)
    neighborhood = models.CharField('Bairro', max_length=100, blank=True)
    city = models.CharField('Cidade', max_length=100, blank=True)
    state = models.CharField('UF', max_length=2, choices=STATE_CHOICES, blank=True)

    is_active = models.BooleanField('Ativo?', default=True, db_index=True)
    deactivated_at = models.DateTimeField('Desativado em', null=True, blank=True)
    deactivated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='companies_deactivated',
        verbose_name='Desativado por'
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Última atualização', auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='companies_updates',
        verbose_name='Atualizado por'
    )
    
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='Membership',
        related_name='companies'
    )

    objects = models.Manager()
    active = ActiveCompanyManager()

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['trade_name', 'legal_name']

    def __str__(self):
        return self.trade_name if self.trade_name else self.legal_name

    def soft_delete(self, user=None):
        self.is_active = False
        self.deactivated_at = timezone.now()
        self.deactivated_by = user
        self.save(update_fields=['is_active', 'deactivated_at', 'deactivated_by'])
        self.memberships.update(is_active=False)

    def reactivate(self):
        self.is_active = True
        self.deactivated_at = None
        self.deactivated_by = None
        self.save(update_fields=['is_active', 'deactivated_at', 'deactivated_by'])


class Membership(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_FINANCIAL = 'financial'
    ROLE_BROKER = 'broker'
    
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Administrador'),
        (ROLE_FINANCIAL, 'Financeiro'),
        (ROLE_BROKER, 'Corretor'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.PROTECT,
        related_name='memberships'
    )
    
    role = models.CharField('Cargo / Perfil', max_length=20, choices=ROLE_CHOICES, default=ROLE_BROKER)
    is_active = models.BooleanField('Ativo?', default=True)
    date_joined = models.DateTimeField('Entrou em', auto_now_add=True)

    class Meta:
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'
        unique_together = ('user', 'company')

    def __str__(self):
        return f"{self.user.email} - {self.company} ({self.get_role_display()})"


class Partner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='partners_list')
    
    name = models.CharField('Nome Completo', max_length=255)
    cpf = models.CharField('CPF', max_length=14)
    email = models.EmailField('Email', blank=True)
    phone = models.CharField('Telefone', max_length=20, blank=True)
    
    class Meta:
        verbose_name = 'Sócio'
        verbose_name_plural = 'Sócios'

    def __str__(self):
        return self.name