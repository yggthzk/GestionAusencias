from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='core/iniciosesion.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('solicitar/', views.crear_solicitud, name='crear_solicitud'),
    path('admin-panel/', views.panel_admin, name='panel_admin'),
    path('gestionar/<int:solicitud_id>/<str:accion>/', views.gestionar_solicitud, name='gestionar_solicitud'),
]