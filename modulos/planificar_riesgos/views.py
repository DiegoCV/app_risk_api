from django.http import Http404
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

from .serializers import CategoriaRbsSerializer
from .serializers import SubCategoriaRbsSerializer
from .serializers import CategoriaRbsSerializerInsert

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
