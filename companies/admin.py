from django.contrib import admin
from .models import Company, Membership

class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0 # Começa sem linhas extras para ficar limpo
    autocomplete_fields = ['user']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # Colunas da tabela
    list_display = ['get_name', 'cnpj', 'city', 'state', 'updated_at', 'updated_by']
    
    # Filtros laterais
    list_filter = ['state', 'created_at']
    
    # Campo de busca
    search_fields = ['legal_name', 'trade_name', 'cnpj']
    
    # Organização do Formulário (Abas visuais)
    fieldsets = (
        ('Identificação', {
            'fields': ('cnpj', 'legal_name', 'trade_name', 'state_registration')
        }),
        ('Sócios', {
            'fields': ('partners',)
        }),
        ('Contato', {
            'fields': ('email', 'phone', 'website')
        }),
        ('Endereço', {
            'fields': ('zip_code', 'address', 'number', 'complement', 'neighborhood', 'city', 'state')
        }),
        ('Auditoria', {
            'fields': ('updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',) # Esconde essa parte por padrão
        }),
    )
    
    # Campos que não podem ser editados manualmente
    readonly_fields = ['created_at', 'updated_at', 'updated_by']
    
    inlines = [MembershipInline]

    def get_name(self, obj):
        return str(obj)
    get_name.short_description = 'Empresa'

    # --- O PULO DO GATO ---
    # Sobrescrevemos o método salvar para preencher o 'updated_by'
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'company']
    search_fields = ['user__email', 'user__name', 'company__legal_name']
    autocomplete_fields = ['user', 'company']