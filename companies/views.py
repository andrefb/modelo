from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction # Importante para salvar Pai e Filhos juntos
from .forms import CompanyCreateForm, PartnerFormSet # Importamos o Formset aqui
from .models import Membership
from .decorators import role_required

@login_required
def create_company(request):
    # Lógica: Se o usuário postar dados
    if request.method == 'POST':
        form = CompanyCreateForm(request.POST)
        formset = PartnerFormSet(request.POST) # Pega os dados dos sócios
        
        # Valida tanto a empresa quanto a lista de sócios
        if form.is_valid() and formset.is_valid():
            with transaction.atomic(): # Garante que salva tudo ou nada
                # 1. Salva a empresa
                company = form.save(commit=False)
                company.updated_by = request.user
                company.save()
                
                # 2. Cria o vínculo de Admin
                Membership.objects.create(
                    user=request.user,
                    company=company,
                    role=Membership.ROLE_ADMIN,
                    is_active=True
                )
                
                # 3. Salva os sócios vinculados a essa empresa
                formset.instance = company
                formset.save()
                
            messages.success(request, 'Empresa e sócios cadastrados com sucesso!')
            return redirect('home')
    else:
        # Lógica: Se for o primeiro acesso (GET)
        form = CompanyCreateForm()
        formset = PartnerFormSet() # Formset vazio para adicionar itens

    return render(request, 'companies/create_company.html', {
        'form': form, 
        'formset': formset
    })

@login_required
@role_required([Membership.ROLE_ADMIN, Membership.ROLE_FINANCIAL])
def company_detail(request):
    # Esta é a view que estava faltando e causando o erro!
    # O middleware já colocou a empresa em request.company
    return render(request, 'companies/company_detail.html', {'company': request.company})

@login_required
@role_required([Membership.ROLE_ADMIN, Membership.ROLE_FINANCIAL])
def company_update(request):
    company = request.company
    
    if request.method == 'POST':
        form = CompanyCreateForm(request.POST, instance=company)
        # Passamos 'instance=company' para o formset saber quais sócios carregar
        formset = PartnerFormSet(request.POST, instance=company) 
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                company = form.save(commit=False)
                company.updated_by = request.user
                company.save()
                
                formset.save() # Salva edições, novos e deleções
            
            messages.success(request, 'Dados atualizados com sucesso!')
            return redirect('company_detail')
    else:
        form = CompanyCreateForm(instance=company)
        formset = PartnerFormSet(instance=company)

    return render(request, 'companies/company_update.html', {
        'form': form,
        'formset': formset
    })