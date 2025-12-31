from django.urls import path
from . import views

urlpatterns = [
    path('tratamiento/<int:cita_id>/', views.registrar_tratamiento, name='registrar_tratamiento'),

    path('eliminar_cita/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),  # ← esta faltaba

    path('editar_cita/<int:cita_id>/', views.editar_cita, name='editar_cita'),  # ← esta faltaba

    path('mis_citas/<int:dueno_id>/', views.mis_citas, name='mis_citas'),

    path('get_veterinarios/', views.get_veterinarios, name='get_veterinarios'),

    path('veterinario_login/', views.veterinario_login, name='veterinario_login'),
    path('', views.bienvenida, name='bienvenida'),
    path('agendar/', views.agendar_cita, name='agendar_cita'),
    path('admin_portal/', views.admin_portal, name='admin_portal'),
    path('veterinario_portal/', views.veterinario_portal, name='veterinario_portal'),
    path('editar_veterinario/<int:id>/', views.editar_veterinario, name='editar_veterinario'),
    path('eliminar_veterinario/<int:id>/', views.eliminar_veterinario, name='eliminar_veterinario'),

]


