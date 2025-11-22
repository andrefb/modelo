from django.shortcuts import redirect
from django.urls import reverse
from .models import Membership, Company

class CompanyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Se não estiver logado, passa
        if not request.user.is_authenticated:
            return self.get_response(request)

        # 2. Rotas isentas
        path = request.path_info
        exempt_paths = [
            reverse('create_company'),
            '/admin/',
            '/accounts/logout/',
            '/static/',
            '/media/',
        ]
        
        if any(path.startswith(p) for p in exempt_paths):
            return self.get_response(request)

        # 3. Busca Empresa na Sessão
        company_id = request.session.get('company_id')
        active_company = None
        membership = None # Variável auxiliar

        if company_id:
            try:
                membership = Membership.objects.get(user=request.user, company__id=company_id, is_active=True)
                active_company = membership.company
            except Membership.DoesNotExist:
                del request.session['company_id']

        # 4. Fallback: Busca a primeira do banco se não achou na sessão
        if not active_company:
            membership = Membership.objects.filter(user=request.user, is_active=True).first()
            if membership:
                active_company = membership.company
                request.session['company_id'] = str(active_company.id)

        # 5. DECISÃO FINAL (A lógica corrigida)
        if active_company:
            # SUCESSO: Temos uma empresa
            request.company = active_company
            
            # Garante que o request.membership esteja preenchido
            if membership:
                request.membership = membership
            else:
                # Caso raro onde active_company existe mas a var membership se perdeu
                try:
                    request.membership = Membership.objects.get(
                        user=request.user, 
                        company=active_company, 
                        is_active=True
                    )
                except Membership.DoesNotExist:
                    request.membership = None
        else:
            # FRACASSO: Não tem empresa nenhuma -> Redireciona
            # (Note que este ELSE agora está alinhado com o IF ACTIVE_COMPANY)
            return redirect('create_company')

        response = self.get_response(request)
        return response