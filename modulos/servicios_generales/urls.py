from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
# urls de gerentes
    path('gerente/', views.RegistrarGerente.as_view()),
    path('gerente/usuario/', views.ValidarUsuario.as_view()),
    path('gerente/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('gerente/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
# urls de proyectos
    path('proyecto/', views.CrearProyecto.as_view()),
    path('proyecto/validar_nombre/<str:proyecto_nombre>/', views.ValidarNombreProyecto.as_view()),
    path('proyecto/actualizar/<str:proyecto_nombre>/', views.ActualizarProyecto.as_view()),
    path('proyecto/listar/', views.ListarProyectos.as_view()),
# urls de categorias
    path('categoria/', views.RegistrarCategoria.as_view()),
    path('categoria/eliminar/<int:categoria_id>/', views.EliminarCategoria.as_view()),
    path('categoria/listar/', views.ListarCategorias.as_view()),
    path('categoria/actualizar/<int:categoria_id>/', views.ActualizarCategoria.as_view()),
# urls de SubCategorias
    path('sub_categoria/', views.RegistrarSubCategoria.as_view()),
    path('sub_categoria/listar/', views.ListarALLSubCategorias.as_view()),
    path('sub_categoria/listar/categoria/<int:categoria_id>/', views.ListarSubCategorias.as_view()),
    path('sub_categoria/actualizar/<int:pk_sub_categoria>/', views.ActualizarSubCategoria.as_view()),
    path('sub_categoria/eliminar/<int:pk_sub_categoria>/', views.EliminarSubCategoria.as_view()),
# urls de riesgo
    path('riesgo/', views.RegistrarRiesgo.as_view()),
    path('riesgo/listar/sub_categoria/<int:sub_categoria_id>/', views.ListarRiesgosPorSubcategoria.as_view()),
    path('riesgo/actualizar/<int:riesgo_id>/', views.ActualizarRiesgo.as_view()),
# urls de respuestas
    path('respuesta/', views.RegistrarRespuesta.as_view()),
    path('respuesta/riesgo/<int:riesgo_id>/', views.RegistrarRespuestaRiesgo.as_view()),
    path('respuesta/actualizar/<int:respuesta_id>/', views.ActualizarRespuesta.as_view()),
    path('respuesta/eliminar/<int:respuesta_id>/', views.EliminarRespuesta.as_view()),
    path('respuesta/asociar/riesgo/<int:riesgo_id>/', views.AsociarRespuestaRiesgo.as_view()),
    path('respuesta/desasociar/riesgo/', views.DesasociarRespuesta.as_view()),
#urls de tipo recurso
    path('tipo_recurso/', views.RegistrarTipoRecurso.as_view()),
    path('tipo_recurso/listar/', views.ListarTipoRecurso.as_view()),

#urls de Recurso
    path('recurso/tipo_recurso/<int:tipo_recurso_id>/', views.RegistrarRecurso.as_view()),
    path('recurso/listar/', views.ListarRecurso.as_view()),
    path('recurso/actualizar/<int:recurso_id>/', views.ActualizarRecurso.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)










# fin
