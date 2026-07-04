from django.contrib import admin
from django.urls import path
from estoque import views

urlpatterns = [

    # ADMIN

    path('admin/', admin.site.urls),

    # AUTENTICAÇÃO

    path('', views.home, name='home'),

    path(
        'registro/',
        views.registro,
        name='registro'
    ),

    path(
        'logout/',
        views.sair,
        name='logout'
    ),

    # MENU

    path(
        'menu/',
        views.menu,
        name='menu'
    ),

    # ESTOQUE

    path(
        'visualizar/',
        views.visualizar,
        name='visualizar'
    ),

    path(
        'editar/',
        views.editar,
        name='editar'
    ),

    path(
        'adicionar/',
        views.adicionar,
        name='adicionar'
    ),

    path(
        'atualizar/<int:id>/',
        views.atualizar,
        name='atualizar'
    ),

    path(
        'deletar/<int:id>/',
        views.deletar,
        name='deletar'
    ),

    # RELATÓRIOS

    path(
        'relatorios/',
        views.relatorios,
        name='relatorios'
    ),

    # PERFIL

    path(
        'perfil/',
        views.perfil,
        name='perfil'
    ),

    path(
        'excluir-perfil/',
        views.excluir_perfil,
        name='excluir_perfil'
    ),

]