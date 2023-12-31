from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('acidentes', views.acidentes_as_json, name='acidentes-as-json'),
    path('acidentes/filtro_severidade/', views.get_fitro_acidentes_severidade, name='consulta-personalizada'),
    path('acidentes/criar_acidente', views.criar_acidente, name='criar-acidente'),
    path('acidentes/editar/<str:num_boletim>/', views.atualizar_acidente, name='atualizar-acidente'),
    path('acidentes/<str:num_boletim>/', views.obter_acidentes_por_id, name='obter_acidentes_por_id'),
    path('acidentes/ultimos', views.ultimos_acidentes, name='ultimos-acidentes'),
    path('api/getinfocep/<str:cep>/', views.getinfocep, name='get_info_cep'),
    path('acidentes/excluir/<str:num_boletim>/', views.excluir_acidente, name='excluir_acidente'),

] 