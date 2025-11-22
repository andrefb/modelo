from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomSignupForm(SignupForm):
    name = forms.CharField(label='Nome Completo', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Ex: João da Silva'}))
    phone = forms.CharField(label='Telefone', max_length=20, widget=forms.TextInput(attrs={'placeholder': '(11) 99999-9999'}))

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.phone = self.cleaned_data['phone']
        user.save()
        return user

class CustomUserCreationForm(UserCreationForm):
    # Redeclaramos as senhas para o Admin não se perder
    password_1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        strip=False,
        help_text="A senha deve ter pelo menos 8 caracteres."
    )
    password_2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Digite a mesma senha novamente."
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone') # Senhas não entram aqui, mas já estão declaradas acima

    def save(self, commit=True):
        # Garante que a senha seja salva criptografada
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password_1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone')