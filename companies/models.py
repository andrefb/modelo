from django.db import models
from django.conf import settings
import uuid

class Company(models.Model):
    # Lista de Estados Brasileiros para o Select
    STATE_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # --- Dados Obrigatórios ---
    legal_name = models.CharField('Razão Social', max_length=255)
    cnpj = models.CharField('CNPJ', max_length=20, unique=True) # Ideal usar máscara no front
    
    # --- Dados Opcionais ---
    trade_name = models.CharField('Nome Fantasia', max_length=255, blank=True)
    state_registration = models.CharField('Inscrição Estadual', max_length=20, blank=True)
    
    

    # --- Contato ---
    phone = models.CharField('Telefone', max_length=20, blank=True)
    email = models.EmailField('Email Comercial', blank=True)
    website = models.URLField('Site', blank=True)
    
    # --- Endereço Padrão BR ---
    zip_code = models.CharField('CEP', max_length=10, blank=True)
    address = models.CharField('Endereço (Logradouro)', max_length=255, blank=True)
    number = models.CharField('Número', max_length=20, blank=True)
    complement = models.CharField('Complemento', max_length=100, blank=True)
    neighborhood = models.CharField('Bairro', max_length=100, blank=True)
    city = models.CharField('Cidade', max_length=100, blank=True)
    state = models.CharField('Estado', max_length=2, choices=STATE_CHOICES, blank=True)

    # --- Auditoria ---
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Última atualização', auto_now=True) # Atualiza data sozinho
    
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Se o usuário for deletado, mantemos o histórico
        null=True, blank=True,
        related_name='companies_updates',
        verbose_name='Atualizado por'
    )
    
    # --- Relação com Usuários ---
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='Membership',
        related_name='companies'
    )

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['trade_name', 'legal_name']

    def __str__(self):
        # Retorna o Fantasia. Se não tiver, retorna a Razão Social
        return self.trade_name if self.trade_name else self.legal_name


class Membership(models.Model):
    # ... (O Membership continua IGUAL ao anterior) ...
    ROLE_ADMIN = 'admin'
    ROLE_FINANCIAL = 'financial'
    ROLE_BROKER = 'broker'
    
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Administrador'),
        (ROLE_FINANCIAL, 'Financeiro'),
        (ROLE_BROKER, 'Corretor'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField('Cargo / Perfil', max_length=20, choices=ROLE_CHOICES, default=ROLE_BROKER)
    is_active = models.BooleanField('Ativo?', default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'
        unique_together = ('user', 'company')

    def __str__(self):
        return f"{self.user.email} - {self.company} ({self.get_role_display()})"
    
    # ... (Classe Company acima)

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