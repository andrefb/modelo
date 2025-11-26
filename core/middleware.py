# core/middleware.py
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        # [MELHORIA SÊNIOR] Converter para TUPLA para performance nativa do CPython
        # Adicionei '/health/' para monitoramento de servidores futuros
        self.public_paths = tuple([
            '/accounts/', 
            '/admin/',     
            '/static/',    
            '/media/',
            '/health/',  # Rota vital para Deploy (Load Balancers)
            '/__debug__/', # Caso use Django Debug Toolbar no futuro
        ])

    def __call__(self, request):
        # Otimização: Resolvemos a verificação em uma linha C-level
        if not request.user.is_authenticated and not request.path_info.startswith(self.public_paths):
            
            # [UX] Adiciona o ?next=/url-que-ele-queria para redirecionar de volta após login
            return redirect(f"{settings.LOGIN_URL}?next={request.path_info}")

        return self.get_response(request)