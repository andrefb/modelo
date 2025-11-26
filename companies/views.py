from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import CompanyCreateForm, PartnerFormSet
from .models import Membership
from .decorators import role_required

@login_required
def create_company(request):
    # [SEGURANÇA] Se o usuário já tem uma empresa ativa, não deixa criar outra (Regra de Negócio MVP)
    # Se no futuro você quiser permitir multi-empresas, é só apagar este bloco if.
    if request.user.memberships.filter(is_active=True).exists():
        return redirect('home')

    if request.method == 'POST':
        form = CompanyCreateForm(request.POST)
        formset = PartnerFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                # 1. Salva a empresa
                company = form.save(commit=False)
                company.updated_by = request.user
                company.save()
                
                # 2. O PULO DO GATO: Define quem criou como ADMIN
                Membership.objects.create(
                    user=request.user,
                    company=company,
                    role=Membership.ROLE_ADMIN, # <--- Garante o poder total
                    is_active=True
                )
                
                # 3. Salva os sócios
                formset.instance = company
                formset.save()

                # 4. [MELHORIA] Já define essa empresa na sessão do usuário
                # Assim o middleware não precisa adivinhar na próxima tela
                request.session['company_id'] = str(company.id)
                
            messages.success(request, 'Empresa configurada com sucesso!')
            return redirect('home')
    else:
        form = CompanyCreateForm()
        formset = PartnerFormSet()

    return render(request, 'companies/create_company.html', {
        'form': form, 
        'formset': formset
    })

@login_required
@role_required([Membership.ROLE_ADMIN, Membership.ROLE_FINANCIAL])
def company_detail(request):
    return render(request, 'companies/company_detail.html', {'company': request.company})

@login_required
@role_required([Membership.ROLE_ADMIN, Membership.ROLE_FINANCIAL])
def company_update(request):
    company = request.company
    
    if request.method == 'POST':
        form = CompanyCreateForm(request.POST, instance=company)
        formset = PartnerFormSet(request.POST, instance=company) 
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                company = form.save(commit=False)
                company.updated_by = request.user
                company.save()
                formset.save()
            
            messages.success(request, 'Dados atualizados com sucesso!')
            return redirect('company_detail')
    else:
        form = CompanyCreateForm(instance=company)
        formset = PartnerFormSet(instance=company)

    return render(request, 'companies/company_update.html', {
        'form': form,
        'formset': formset
    })