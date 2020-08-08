from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [

    #BORRAr
    path('excel/', views.ExampleViewSet.as_view()),
    #METODOS RELACIONADOS A LA RBS DE UN PROYECTO
    path('rbs/proyecto/<int:proyecto_id>/', views.ObtenerRbs.as_view()),
    path('rbs/asociar_categorias/', views.AsociarCategorias.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)
