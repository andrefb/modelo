from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.create_company, name='create_company'),
    path('profile/', views.company_detail, name='company_detail'),
    path('profile/edit/', views.company_update, name='company_update'),
]