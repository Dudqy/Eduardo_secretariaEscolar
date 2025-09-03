from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard-professor/', views.dashboard_professor, name='dashboard_professor'),
    path('desempenho/', views.desempenho, name='desempenho'),
    path('historico/', views.historico, name='historico'),
    path('historico/pdf/', views.historico_pdf, name='historico_pdf'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path('painel-faltas/', views.painel_faltas, name='painel_faltas'),
]
