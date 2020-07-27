import hashlib
import copy

from django.http import Http404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Gerente
from .models import Proyecto
from .models import Categoria
from .models import SubCategoria

from .serializers import GerenteSerializer
from .serializers import ProyectoSerializerInsert
from .serializers import ProyectoSerializer
from .serializers import CategoriaSerializer
from .serializers import SubCategoriaSerializer
from .serializers import MyTokenObtainPairSerializer
from .serializers import RiesgoSerializer

from .utils import decodificar_jwt_token
from .utils import get_gerente_by_username
from .utils import get_gerente_id
from .utils import get_gerente_by_id

"""
////////////////////////////////////////////////////////////////////////////
    HISTORIA DE USARIO N° 1
/////////////////////////////////////////////////////////////////////////////
"""
class RegistrarGerente(APIView):

    def post(self, request, format=None):
        """request.data['gerente_password'] = hashlib.sha1(request.data['gerente_password'].encode("utf-8")).hexdigest()"""
        serializer = GerenteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            gerente_id = copy.deepcopy(serializer.data['gerente_id'])
            self.registrarUsuario(request.data['gerente_usuario'], request.data['gerente_correo'], request.data['gerente_password'], request.data['gerente_nombre'], gerente_id)
            return Response({"msg" : "Gerente registrado"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def registrarUsuario(self, usuario, correo, password, nombre, gerente_id):
        user = User.objects.create_user(username=usuario, email=correo, password = password, first_name = nombre, id = gerente_id)
        user.save()


class ValidarUsuario(APIView):

    def post(self, request, format=None):
        usuario = request.data['usuario']
        try:
            Gerente.objects.using('riesgos').get(gerente_usuario=usuario)
            return Response({'msg':'usuario en uso'}, status=status.HTTP_400_BAD_REQUEST)
        except Gerente.DoesNotExist:
            return Response({'msg':'usuario diponible'}, status=status.HTTP_200_OK)


"""
////////////////////////////////////////////////////////////////////////////
    HISTORIA DE USARIO N° 2
/////////////////////////////////////////////////////////////////////////////
"""


class CrearProyecto(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = ProyectoSerializerInsert(data=request.data)
        if serializer.is_valid():
            username = decodificar_jwt_token(request)["username"]
            serializer.create(request.data, username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActualizarProyecto(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, request, proyecto_nombre):
        try:
            gerente = get_gerente_by_id(request)
            return Proyecto.objects.get(proyecto_nombre = proyecto_nombre, gerente = gerente)
        except Proyecto.DoesNotExist:
            raise Http404

    def put(self, request, proyecto_nombre, format=None):
        #request.data["proyecto_nombre"] = proyecto_nombre
        proyecto = self.get_object(request, proyecto_nombre)
        serializer = ProyectoSerializerInsert(proyecto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidarNombreProyecto(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, proyecto_nombre, format=None):
        gerente = get_gerente_by_username(request)
        try:
            Proyecto.objects.using('riesgos').get(proyecto_nombre = proyecto_nombre, gerente=gerente)
            return Response({'msg':'nombre de proyecto en uso'}, status=status.HTTP_400_BAD_REQUEST)
        except Proyecto.DoesNotExist:
            return Response({'msg':'nombre de proyecto diponible'}, status=status.HTTP_200_OK)


class ListarProyectos(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        gerente = get_gerente_by_id(request)
        proyectos = Proyecto.objects.filter(gerente = gerente)
        serializer = ProyectoSerializer(proyectos, many=True)
        return Response(serializer.data)

"""
////////////////////////////////////////////////////////////////////////////
    HISTORIA DE USUARIO N° 3
/////////////////////////////////////////////////////////////////////////////
"""

""" ***
    Categoria
    ***
"""
class RegistrarCategoria(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            gerente_id = get_gerente_id(request)
            serializer.create(request.data, gerente_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarCategorias(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        gerente = get_gerente_by_id(request)
        categorias = Categoria.objects.filter(gerente = gerente)
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)


class ActualizarCategoria(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, request, categoria_id):
        try:
            gerente = get_gerente_by_id(request)
            return Categoria.objects.get(categoria_id = categoria_id, gerente = gerente)
        except Categoria.DoesNotExist:
            raise Http404

    def put(self, request, categoria_id, format=None):
        categoria = self.get_object(request, categoria_id)
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#En espera
class EliminarCategoria(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, request, categoria_id):
        try:
            gerente = get_gerente_by_id(request)
            return Categoria.objects.get(categoria_id = categoria_id, gerente = gerente)
        except Categoria.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
    ***
    SubCategoria
    ***
"""
class RegistrarSubCategoria(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = SubCategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
    ***
    Riesgo
    ***
"""
class RegistrarRiesgo(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = RiesgoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
////////////////////////////////////////////////////////////////////////////
    CONFIGURACION DEL TOKEN
/////////////////////////////////////////////////////////////////////////////
"""

""" Esta clase permite agregar mis datos al token"""
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
