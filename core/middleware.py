# core/middleware.py
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Lista de caminhos permitidos (Públicos)
        # Precisamos deixar o usuário acessar a tela de login, cadastro e o admin
        public_paths = [
            '/accounts/',  # Rotas do Allauth (Login, Signup, Reset Senha)
            '/admin/',     # Django Admin
            '/static/',    # Arquivos estáticos (CSS/JS)
            '/media/',     # Uploads
        ]

        # 2. Verifica se o caminho atual começa com algum dos permitidos
        path = request.path_info
        is_public = any(path.startswith(p) for p in public_paths)

        # 3. A Lógica do Porteiro:
        # Se o usuário NÃO está logado E a página NÃO é pública...
        if not request.user.is_authenticated and not is_public:
            # ...Redireciona para o Login
            return redirect(settings.LOGIN_URL)

        # Se passou no teste, segue o fluxo normal
        response = self.get_response(request)
        return response