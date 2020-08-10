from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [

    #BORRAr
    path('excel/', views.ExampleViewSet.as_view()),
    #METODOS RELACIONADOS A LA RBS DE UN PROYECTO
    path('rbs/proyecto/<int:proyecto_id>/', views.ObtenerRbs.as_view()),
    #METODOS RELACIONADOS CON CATEGORIA RBS
    path('rbs/asociar_categorias/', views.AsociarCategorias.as_view()),
    path('rbs/desasociar_categorias/', views.DesasociarCategorias.as_view()),
    #METODOS RELACIONADOS A SUBCATEGORIA RBS
    path('rbs/asociar_sub_categorias/', views.AsociarSubCategorias.as_view()),
    path('rbs/desasociar_sub_categorias/', views.DesasociarSubCategorias.as_view()),
    #RESPONSABLE
    path('responsable/', views.RegistrarResponsable.as_view()),
    path('responsable/listar/', views.ListarResponsablePorProyecto.as_view()),
    #RIESGO
    path('riesgo/rbs/', views.RegistrarRiesgoAsosiadoSubcategoriaRbs.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)

















#B
