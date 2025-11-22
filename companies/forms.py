from django import forms
from django.forms import inlineformset_factory # <--- Importe isso
from .models import Company, Partner

class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'cnpj', 'legal_name', 'trade_name', 'state_registration',
            'phone', 'email', 'website',
            'zip_code', 'address', 'number', 'complement', 'neighborhood', 'city', 'state',
            # Note que removemos 'partners' daqui, pois agora é uma tabela separada
        ]

# Formulário individual do Sócio
class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'cpf', 'email', 'phone']

# A "Fábrica" de lista de sócios
PartnerFormSet = inlineformset_factory(
    Company, 
    Partner,
    form=PartnerForm,
    extra=0,          # Começa sem linhas vazias (adicionamos via botão)
    can_delete=True   # Permite deletar
)