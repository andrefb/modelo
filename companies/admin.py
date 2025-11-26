from django.contrib import admin
from . models import Company, Membership, Partner


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0
    autocomplete_fields = ['user']
    readonly_fields = ['date_joined']
    fields = ['user', 'role', 'is_active', 'date_joined']


class PartnerInline(admin.TabularInline):
    model = Partner
    extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # --- Listagem ---
    list_display = ['get_name', 'cnpj', 'city', 'state', 'is_active', 'member_count', 'updated_at']
    list_filter = ['is_active', 'state', 'created_at']
    search_fields = ['legal_name', 'trade_name', 'cnpj']
    
    # --- Formulário ---
    fieldsets = (
        ('Identificação', {
            'fields': ('cnpj', 'legal_name', 'trade_name', 'state_registration')
        }),
        ('Contato', {
            'fields': ('email', 'phone', 'website')
        }),
        ('Endereço', {
            'fields': ('zip_code', 'address', 'number', 'complement', 'neighborhood', 'city', 'state')
        }),
        ('Status', {
            'fields': ('is_active',),
            'description': '⚠️ Desativar a empresa desativa automaticamente todos os membros.'
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'updated_by', 'deactivated_at', 'deactivated_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'updated_by', 'deactivated_at', 'deactivated_by']
    inlines = [MembershipInline, PartnerInline]
    actions = ['deactivate_companies', 'reactivate_companies']

    def get_name(self, obj):
        return str(obj)
    get_name.short_description = 'Empresa'

    def member_count(self, obj):
        return obj.memberships.filter(is_active=True).count()
    member_count.short_description = 'Membros Ativos'

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        """Bloqueia deleção - força uso do soft delete"""
        return False

    @admin.action(description="🚫 Desativar empresas selecionadas")
    def deactivate_companies(self, request, queryset):
        count = 0
        for company in queryset. filter(is_active=True):
            company.soft_delete(user=request.user)
            count += 1
        self. message_user(request, f"✅ {count} empresa(s) desativada(s).  Membros também foram desativados.")

    @admin.action(description="✅ Reativar empresas selecionadas")
    def reactivate_companies(self, request, queryset):
        count = 0
        for company in queryset.filter(is_active=False):
            company.reactivate()
            count += 1
        self.message_user(request, f"✅ {count} empresa(s) reativada(s). Reative os membros manualmente se necessário.")


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    # --- Listagem ---
    list_display = ['user', 'company', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'company']
    search_fields = ['user__email', 'user__name', 'company__legal_name']
    autocomplete_fields = ['user', 'company']
    
    # --- Ações ---
    actions = ['deactivate_members', 'reactivate_members']

    @admin.action(description="🚫 Desativar membros selecionados")
    def deactivate_members(self, request, queryset):
        count = queryset.filter(is_active=True).update(is_active=False)
        self.message_user(request, f"✅ {count} membro(s) desativado(s).")

    @admin.action(description="✅ Reativar membros selecionados")
    def reactivate_members(self, request, queryset):
        # Só reativa se a empresa também estiver ativa
        count = 0
        for membership in queryset.filter(is_active=False):
            if membership.company.is_active:
                membership.is_active = True
                membership. save(update_fields=['is_active'])
                count += 1
            else:
                self.message_user(
                    request, 
                    f"⚠️ {membership.user.email} não foi reativado pois a empresa {membership.company} está inativa.",
                    level='WARNING'
                )
        if count:
            self.message_user(request, f"✅ {count} membro(s) reativado(s).")


@admin.register(Partner)
class PartnerAdmin(admin. ModelAdmin):
    list_display = ['name', 'cpf', 'company', 'email', 'phone']
    list_filter = ['company']
    search_fields = ['name', 'cpf', 'company__legal_name']
    autocomplete_fields = ['company']