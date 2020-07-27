from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path('gerente/', views.RegistrarGerente.as_view()),
    path('gerente/usuario/', views.ValidarUsuario.as_view()),
    path('gerente/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('gerente/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('proyecto/', views.CrearProyecto.as_view()),
    path('proyecto/validar_nombre/<str:proyecto_nombre>/', views.ValidarNombreProyecto.as_view()),
    path('proyecto/actualizar/<str:proyecto_nombre>/', views.ActualizarProyecto.as_view()),
    path('proyecto/listar/', views.ListarProyectos.as_view()),
    path('categoria/', views.RegistrarCategoria.as_view()),
    path('categoria/listar/', views.ListarCategorias.as_view()),
    path('categoria/actualizar/<int:categoria_id>/', views.ActualizarCategoria.as_view()),
    path('sub_categoria/', views.RegistrarSubCategoria.as_view()),
    path('riesgo/', views.RegistrarRiesgo.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
