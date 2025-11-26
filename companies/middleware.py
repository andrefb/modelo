from django.shortcuts import redirect
from django.urls import reverse
from . models import Membership


class CompanyMiddleware:
    """
    Middleware que injeta a empresa ativa no request.
    Só permite acesso se usuário E empresa E membership estiverem ativos.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Se não estiver logado, passa direto
        if not request.user.is_authenticated:
            return self.get_response(request)

        # 2.  Rotas isentas
        path = request.path_info
        exempt_paths = [
            reverse('create_company'),
            '/admin/',
            '/accounts/',
            '/static/',
            '/media/',
        ]
        
        if any(path.startswith(p) for p in exempt_paths):
            return self.get_response(request)

        # 3. Tenta pegar empresa da sessão
        company_id = request.session.get('company_id')
        active_company = None
        membership = None

        if company_id:
            try:
                membership = Membership.objects.select_related('company').get(
                    user=request.user,
                    company__id=company_id,
                    company__is_active=True,
                    is_active=True
                )
                active_company = membership. company
            except Membership.DoesNotExist:
                if 'company_id' in request. session:
                    del request. session['company_id']

        # 4.  Fallback: primeira empresa ativa
        if not active_company:
            membership = Membership.objects.select_related('company').filter(
                user=request.user,
                company__is_active=True,
                is_active=True
            ).first()
            
            if membership:
                active_company = membership.company
                request.session['company_id'] = str(active_company.id)

        # 5. Decisão
        if active_company:
            request.company = active_company
            request.membership = membership
        else:
            return redirect('create_company')

        return self.get_response(request)