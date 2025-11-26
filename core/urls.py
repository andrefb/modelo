
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

# ✅ Opção 1: Definir a função
def trigger_error(request):
    division_by_zero = 1 / 0  # Proposital para testar Sentry



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('companies/', include('companies.urls')), # <--- Adicione isso
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('sentry-debug/', trigger_error), 
]
