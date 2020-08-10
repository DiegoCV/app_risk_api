from django.http import Http404
from django.db import transaction
from django.http import HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Rbs
from .models import Proyecto
from .models import Categoria
from .models import SubCategoria
from .models import CategoriaRbs
from .models import SubCategoriaRbs
from .models import Responsable
from .models import RiesgoRbs

from .serializers import CategoriaRbsSerializer
from .serializers import CategoriaRbsSerializerInsert
from .serializers import SubCategoriaRbsSerializer
from .serializers import SubCategoriaRbsSerializerInsert
from .serializers import ResponsableSerializer
from .serializers import ResponsableSerializerList
from .serializers import RiesgoSerializer

from .utils import get_gerente_id
from .utils import get_gerente_by_id

"""
////////////////////////////////////////////////////////////////////////////
    METODOS RELACIONADOS CON LA RBS
/////////////////////////////////////////////////////////////////////////////
"""

class ObtenerRbs(APIView):

    permission_classes = (IsAuthenticated,)

    def get_rbs(self, proyecto_id, gerente_id):
        try:
            rbs = Rbs.objects.raw("SELECT r.rbs_id, r.proyecto_id FROM rbs r INNER JOIN proyecto p ON r.proyecto_id = p.proyecto_id INNER JOIN gerente g ON p.gerente_id = g.gerente_id WHERE p.proyecto_id = %s AND g.gerente_id = %s", [proyecto_id, gerente_id])
            return rbs[0]
        except:
            raise Http404

    def get(self, request, proyecto_id, format=None):
        gerente_id = get_gerente_id(request)
        rbs = self.get_rbs(proyecto_id, gerente_id)
        categorias_rbs = CategoriaRbs.objects.filter(rbs = rbs)
        categorias_rbs_list = []
        for categoria_rbs in categorias_rbs:
            sub_categorias_rbs_list = SubCategoriaRbs.objects.filter(categoria_rbs = categoria_rbs)
            categorias_rbs_list.append({
            "categoria_rbs":CategoriaRbsSerializer(categoria_rbs).data,
            "sub_categorias_rbs":SubCategoriaRbsSerializer(sub_categorias_rbs_list,context={'request': request} ,many=True).data
            })
        return Response(categorias_rbs_list)


"""
////////////////////////////////////////////////////////////////////////////
    METODOS RELACIONADOS CON LA CATEGORIA RBS
/////////////////////////////////////////////////////////////////////////////
"""

class AsociarCategorias(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            proyecto_id = request.data["proyecto_id"]
            gerente_id = get_gerente_id(request)
            categorias_id = request.data["categorias_id"]
            rbs = Rbs.objects.raw("SELECT r.rbs_id, r.proyecto_id FROM rbs r INNER JOIN proyecto p ON r.proyecto_id = p.proyecto_id INNER JOIN gerente g ON p.gerente_id = g.gerente_id WHERE p.proyecto_id = %s AND g.gerente_id = %s", [proyecto_id, gerente_id])[0]
            #print(rbs)
            for categoria_id in categorias_id:
                categoria = Categoria()
                categoria.categoria_id = categoria_id
                e ={"categoria":categoria, "rbs":rbs}
                #print(e)
                r = CategoriaRbsSerializerInsert()
                r.create(datos=e)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as inst:
            print(inst)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DesasociarCategorias(APIView):

    permission_classes = (IsAuthenticated,)

    def delete(self, request, format=None):
        try:
            proyecto_id = request.data["proyecto_id"]
            gerente_id = get_gerente_id(request)
            categorias_rbs_id = request.data["categorias_rbs_id"]
            rbs = Rbs.objects.raw("SELECT r.rbs_id, r.proyecto_id FROM rbs r INNER JOIN proyecto p ON r.proyecto_id = p.proyecto_id INNER JOIN gerente g ON p.gerente_id = g.gerente_id WHERE p.proyecto_id = %s AND g.gerente_id = %s", [proyecto_id, gerente_id])[0]
            for categoria_rbs_id in categorias_rbs_id:
                categoria_rbs = CategoriaRbs.objects.get(categoria_rbs_id = categoria_rbs_id, rbs = rbs)
                categoria_rbs.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as inst:
            print(inst)
            return Response(status=status.HTTP_400_BAD_REQUEST)


"""
////////////////////////////////////////////////////////////////////////////
    METODOS RELACIONADOS CON LA SUB CATEGORIA RBS
/////////////////////////////////////////////////////////////////////////////
"""

class AsociarSubCategorias(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            proyecto_id = request.data["proyecto_id"]
            categoria_rbs_id = request.data["categoria_rbs_id"]
            gerente_id = get_gerente_id(request)
            sub_categorias_id = request.data["sub_categorias_id"]
            rbs = Rbs.objects.raw("SELECT r.rbs_id, r.proyecto_id FROM rbs r INNER JOIN proyecto p ON r.proyecto_id = p.proyecto_id INNER JOIN gerente g ON p.gerente_id = g.gerente_id WHERE p.proyecto_id = %s AND g.gerente_id = %s", [proyecto_id, gerente_id])[0]
            categoria_rbs = CategoriaRbs.objects.get(categoria_rbs_id = categoria_rbs_id, rbs = rbs)
            print(categoria_rbs)
            print(categoria_rbs.categoria)
            for sub_categoria_id in sub_categorias_id:
                sub_categoria = SubCategoria.objects.get(sub_categoria_id = sub_categoria_id, categoria = categoria_rbs.categoria)
                e ={"categoria_rbs":categoria_rbs, "sub_categoria":sub_categoria}
                r = SubCategoriaRbsSerializerInsert()
                r.create(datos=e)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as inst:
            print(inst)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DesasociarSubCategorias(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, request):
        try:
            return Proyecto.objects.get(proyecto_id = request.data["proyecto_id"], gerente = get_gerente_by_id(request))
        except Proyecto.DoesNotExist:
            raise Http404

    def delete(self, request, format=None):
        try:
            proyecto = self.get_object(request)
            sub_categorias_rbs_id = request.data["sub_categorias_rsb_id"]
            for sub_categoria_rbs_id in sub_categorias_rbs_id:
                sub_categoria_rbs = SubCategoriaRbs.objects.raw("SELECT scr.sub_categoria_rbs_id, scr.sub_categoria_id, scr.categoria_rbs_id FROM sub_categoria_rbs scr INNER JOIN categoria_rbs cr ON scr.categoria_rbs_id = cr.categoria_rbs_id INNER JOIN rbs r ON cr.rbs_id = r.rbs_id WHERE sub_categoria_rbs_id = %s AND r.proyecto_id = %s",[sub_categoria_rbs_id, proyecto.proyecto_id])[0]
                sub_categoria_rbs.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as inst:
            print(inst)
            return Response(status=status.HTTP_400_BAD_REQUEST)


"""
////////////////////////////////////////////////////////////////////////////
    METODO DE PRUEBA PARA RESPONSABLES
/////////////////////////////////////////////////////////////////////////////
"""
class RegistrarResponsable(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        proyecto_id = request.data["proyecto"]["proyecto_id"]
        del request.data["proyecto"]["proyecto_id"]
        request.data["proyecto"] = Proyecto(proyecto_id = proyecto_id)
        serializer = ResponsableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarResponsablePorProyecto(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            gerente = get_gerente_by_id(request)
            proyecto = Proyecto.objects.get(proyecto_id = request.data["proyecto_id"], gerente = gerente)
            responsables = Responsable.objects.filter(proyecto = proyecto)
            serializer = ResponsableSerializerList(responsables, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as inst:
            print(inst)
            return Response(status=status.HTTP_400_BAD_REQUEST)


"""
////////////////////////////////////////////////////////////////////////////
    METODO DE PRUEBA PARA RIESGOS
/////////////////////////////////////////////////////////////////////////////
"""
class RegistrarRiesgoAsosiadoSubcategoriaRbs(APIView):

    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request, format=None):
        sql = "SELECT scr.sub_categoria_rbs_id, scr.sub_categoria_id, scr.categoria_rbs_id FROM sub_categoria_rbs scr INNER JOIN categoria_rbs cr ON scr.categoria_rbs_id = cr.categoria_rbs_id INNER JOIN rbs r ON cr.rbs_id = r.rbs_id INNER JOIN proyecto p ON r.proyecto_id = p.proyecto_id INNER JOIN gerente g ON p.gerente_id = g.gerente_id WHERE scr.sub_categoria_rbs_id = %s AND g.gerente_id = %s"
        sub_categoria_rbs = SubCategoriaRbs.objects.raw(sql,[request.data["sub_categoria_rbs_id"], get_gerente_id(request)])[0]
        del request.data["sub_categoria_rbs_id"]
        request.data["sub_categoria_id"] = sub_categoria_rbs.sub_categoria_id
        serializer = RiesgoSerializer(data=request.data)
        if serializer.is_valid():
            riesgo = serializer.create(request.data)
            riesgo_rbs = RiesgoRbs(riesgo = riesgo, sub_categoria_rbs = sub_categoria_rbs)
            riesgo_rbs.save()
            return Response({"msg": "registro exitoso"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
////////////////////////////////////////////////////////////////////////////
    METODO DE PRUEBA PARA RETORNAR UN EXCEL
/////////////////////////////////////////////////////////////////////////////
"""

class ExampleViewSet(APIView):

    def get(self, request, format=None):
        ur = 'C:\\Users\\DiegoCV\\Documents\\tesis\\tesis\\codigo\\ufps_risk_api\\app_risk_api\\modulos\\servicios_generales\\test.xlsx'
        zip_file = open(ur, 'rb')
        print(zip_file)
        t = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(zip_file, content_type=t)
        response['Content-Disposition'] = 'attachment; filename="%s"' % 'CDX_COMPOSITES_20140626.xlsx'

        return response
