from django import forms
from django.forms import inlineformset_factory
from .models import Company, Partner

class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'cnpj', 'legal_name', 'trade_name', 'state_registration',
            'phone', 'phone_2', 'email', 'website',
            'zip_code', 'address', 'number', 'complement', 
            'neighborhood', 'city', 'state',
        ]

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'cpf', 'email', 'phone']

PartnerFormSet = inlineformset_factory(
    Company, 
    Partner,
    form=PartnerForm,
    extra=0,
    can_delete=True
)