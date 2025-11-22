from django.core.exceptions import PermissionDenied
from functools import wraps
from .models import Membership

def role_required(allowed_roles):
    """
    Decorador para restringir acesso baseado no Cargo (Role) na empresa atual.
    Uso: @role_required(['admin', 'financial'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # O middleware já garante que request.membership existe se tiver empresa
            if not request.membership:
                 raise PermissionDenied
            
            if request.membership.role not in allowed_roles:
                # Opcional: Redirecionar para uma página de "Sem Permissão" amigável
                # ou apenas lançar o erro 403 padrão do Django
                raise PermissionDenied("Você não tem permissão para acessar esta área.")
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator