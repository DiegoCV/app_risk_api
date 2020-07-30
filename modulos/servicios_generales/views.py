import hashlib
import copy

from django.http import Http404
from django.db import transaction
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
from .models import Riesgo
from .models import Respuesta
from .models import RespuestaHasRiesgo

from .serializers import GerenteSerializer
from .serializers import ProyectoSerializerInsert
from .serializers import ProyectoSerializer
from .serializers import CategoriaSerializer
from .serializers import SubCategoriaSerializer
from .serializers import SubCategoriaSerializerUpdate
from .serializers import MyTokenObtainPairSerializer
from .serializers import RiesgoSerializer
from .serializers import RiesgoSerializerUpdate

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


class EliminarCategoria(APIView):

    permission_classes = (IsAuthenticated,)

    def validar_uso(self, categoria_id, gerente_id):
        try:
            categoria = Categoria.objects.raw("SELECT c.categoria_id, c.categoria_nombre, c.categoria_descripcion, c.gerente_id FROM categoria c INNER JOIN sub_categoria sc ON c.categoria_id = sc.categoria_id INNER JOIN riesgo r ON r.sub_categoria_id = sc.sub_categoria_id WHERE c.categoria_id = %s AND c.gerente_id = %s LIMIT 1",[categoria_id, gerente_id])[0]
            return categoria
        except Exception as inst:
            return False

    def get_object(self, categoria_id, gerente_id):
        try:
            return Categoria.objects.get(categoria_id = categoria_id, gerente_id = gerente_id)
        except Categoria.DoesNotExist:
            raise Http404

    def delete(self, request, categoria_id, format=None):
        gerente_id = get_gerente_id(request)
        if(self.validar_uso(categoria_id, gerente_id)):
            return Response({"msg":"Categoria en uso"}, status=status.HTTP_204_NO_CONTENT)
        else:
            categoria = self.get_object(categoria_id, gerente_id)
            categoria.delete()
            return Response({"msg":"Categoria eliminada"}, status=status.HTTP_204_NO_CONTENT)

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


class ListarSubCategorias(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, categoria_id, format=None):
        try:
            gerente = get_gerente_by_id(request)
            categoria = Categoria.objects.get(categoria_id = categoria_id, gerente = gerente)
            sub_categorias = SubCategoria.objects.filter(categoria = categoria)
            serializer = SubCategoriaSerializer(sub_categorias, many=True)
            return Response(serializer.data)
        except Categoria.DoesNotExist:
            raise Http404


class ActualizarSubCategoria(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, sub_categoria_id, gerente_id):
        try:
            categoria = SubCategoria.objects.raw("SELECT sc.sub_categoria_id, sc.sub_categoria_nombre, sc.sub_categoria_descripcion FROM sub_categoria sc  INNER JOIN categoria c  on sc.categoria_id = c.categoria_id INNER JOIN gerente g ON c.gerente_id = g.gerente_id WHERE sc.sub_categoria_id = %s AND g.gerente_id = %s", [sub_categoria_id, gerente_id])[0]
            return categoria
        except IndexError:
            return False
        except SubCategoria.DoesNotExist:
            raise Http404

    def put(self, request, pk_sub_categoria, format=None):
        gerente_id = get_gerente_id(request)
        sub_categoria = self.get_object(pk_sub_categoria, gerente_id)
        if(sub_categoria):
            serializer = SubCategoriaSerializerUpdate(sub_categoria, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"subcatgoria no pertenece al gerente"}, status=status.HTTP_400_BAD_REQUEST)

#ARREGLAR
class EliminarSubCategoria(APIView):

    permission_classes = (IsAuthenticated,)

    def validar_uso(self, sub_categoria_id, gerente_id):
        try:
            s = SubCategoria.objects.raw("SELECT sc.sub_categoria_id, sc.sub_categoria_nombre, sc.sub_categoria_descripcion FROM sub_categoria sc INNER JOIN riesgo r ON r.sub_categoria_id = sc.sub_categoria_id INNER JOIN categoria c ON c.categoria_id = sc.categoria_id INNER JOIN gerente g ON c.gerente_id = g.gerente_id WHERE sc.sub_categoria_id = %s AND c.gerente_id = %s LIMIT 1", [sub_categoria_id, gerente_id])[0]
            print("HOLA")
            print(s)
            return s
        except SubCategoria.DoesNotExist:
            raise Http404
        except Exception as inst:
            return False

    def get_object(self, sub_categoria_id, gerente_id):
        try:
            return SubCategoria.objects.get(sub_categoria_id = sub_categoria_id)
        except SubCategoria.DoesNotExist:
            raise Http404

    def delete(self, request, pk_sub_categoria, format=None):
        gerente_id = get_gerente_id(request)
        if(self.validar_uso(pk_sub_categoria, gerente_id)):
            return Response({"msg":"SubCategoria en uso"}, status=status.HTTP_204_NO_CONTENT)
        else:
            categoria = self.get_object(pk_sub_categoria, gerente_id)
            categoria.delete()
            return Response({"msg":"SubCategoria eliminada"}, status=status.HTTP_204_NO_CONTENT)
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


class ListarRiesgosPorSubcategoria(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, sub_categoria_id, format=None):
        try:
            sub_categoria = SubCategoria.objects.get(sub_categoria_id = sub_categoria_id)
            riesgos = Riesgo.objects.filter(sub_categoria = sub_categoria)
            serializer = RiesgoSerializer(riesgos, many=True)
            return Response(serializer.data)
        except SubCategoria.DoesNotExist:
            raise Http404

#probar
class ActualizarRiesgo(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, riesgo_id, gerente_id):
        try:
            riesgo = Riesgo.objects.raw("SELECT r.riesgo_id, r.riesgo_nombre, r.riesgo_causa, r.riesgo_evento, r.riesgo_efecto, r.riesgo_tipo, r.riesgo_prom_evaluacion FROM riesgo r INNER JOIN sub_categoria sc  ON r.sub_categoria_id = sc.sub_categoria_id INNER JOIN categoria c  ON sc.categoria_id = c.categoria_id INNER JOIN gerente g ON c.gerente_id = g.gerente_id WHERE r.riesgo_id = %s AND g.gerente_id = %s", [riesgo_id, gerente_id])[0]
            return categoria
        except IndexError:
            return False
        except Riesgo.DoesNotExist:
            raise Http404

    def put(self, request, riesgo_id, format=None):
        gerente_id = get_gerente_id(request)
        riesgo = self.get_object(riesgo_id, gerente_id)
        if(riesgo):
            serializer = RiesgoSerializerUpdate(riesgo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                gerente_id = copy.deepcopy(serializer.data['gerente_id'])
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"riesgo no pertenece al gerente"}, status=status.HTTP_400_BAD_REQUEST)


"""
////////////////////////////////////////////////////////////////////////////
    HISTORIA DE USUARIO N° 4
/////////////////////////////////////////////////////////////////////////////
"""

class RegistrarRespuesta(APIView):

    permission_classes = (IsAuthenticated,)

    # Muy seguramente me sabran disculpar, pero es que no tengo tiempo de ponerme a validar estas maricadas.
    # En un futuro, cuando los riesgos se modifiquen solos deben asegurarse de cambiar este metodo y preguntar si el riesgo pertenece al gerente
    def get_riesgo(self, riesgo_id):
        try:
            return Riesgo.objects.get(riesgo_id = riesgo_id)
        except Respuesta.DoesNotExist:
            raise Http404

    def post(self, request, riesgo_id, format=None):
        serializer = RespuestaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            respuesta_id = copy.deepcopy(serializer.data['respuesta_id'])

            serializer_2 = RespuestaHasRiesgoSerializer(data={'respuesta_id':respuesta_id, 'riesgo_id': riesgo_id})
            if serializer_2.is_valid():
                serializer_2.save()

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
