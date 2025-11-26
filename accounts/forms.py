from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomSignupForm(SignupForm):
    name = forms.CharField(label='Nome Completo', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Ex: João da Silva'}))
    phone = forms.CharField(label='Telefone', max_length=20, widget=forms.TextInput(attrs={'placeholder': '(11) 99999-9999'}))

    def save(self, request):
        # 1. O Allauth salva o usuário (User instance)
        user = super(CustomSignupForm, self).save(request)
        
        # 2. Nós atualizamos os campos extras
        user.name = self.cleaned_data['name']
        user.phone = self.cleaned_data['phone']
        
        # 3. Salvamos novamente (Update)
        user.save()
        
        return user

# accounts/forms.py
class CustomUserCreationForm(UserCreationForm):
    # NÃO precisa redeclarar!  O UserCreationForm já tem password1 e password2
    
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone')
    
    def clean_password2(self):
        # Validação de confirmação já vem do UserCreationForm
        return super().clean_password2()

    def save(self, commit=True):
        # Garante que a senha seja salva criptografada
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        
        # Remove espaços duplos
        name = ' '.join(name. split())
        
        # Capitaliza (opcional, mas elegante)
        # name = name.title()
        
        if len(name) < 3:
            raise forms.ValidationError('Nome deve ter pelo menos 3 caracteres.')
        
        return name

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone')

