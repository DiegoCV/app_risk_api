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
    path('riesgo/rbs/asociar/', views.AsociarRiesgoRbs.as_view()),
    path('riesgo/rbs/desasociar/', views.DesasociarRiesgoRbs.as_view()),
    #RIESGO RBS
    path('riesgo_rbs/asociar/actividad/', views.AsociarRiesgoRbsActividad.as_view()),
    path('riesgo_rbs/desasociar/actividad/', views.DesasociarRiesgoRbsActividad.as_view()),
    #Respuesta
    path('respuesta/asociar/riesgo_rbs/', views.AsociarRespuestaconRiesgoRbs.as_view()),
    path('respuesta/desasociar/riesgo_rbs/', views.DesasociarRespuestaRbsconRiesgoRbs.as_view()),

    #INFORMES

    path('informe/planificar_riesgos/', views.GenerarRiesgosPorProyecto.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)

















#B
