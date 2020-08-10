from rest_framework import serializers, fields

from .models import Rbs
from .models import Proyecto
from .models import Categoria
from .models import SubCategoria
from .models import CategoriaRbs
from .models import SubCategoriaRbs
from .models import Responsable
from .models import Riesgo


"""
//////////////////////////////////////////////////////
    Serializers relacionados con Categoria
//////////////////////////////////////////////////////
"""
class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    categoria_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Categoria
        fields = ("categoria_id", "categoria_nombre", "categoria_descripcion")


"""
//////////////////////////////////////////////////////
    Serializers relacionados con SubCategoria
//////////////////////////////////////////////////////
"""
class SubCategoriaSerializer(serializers.HyperlinkedModelSerializer):
    sub_categoria_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = SubCategoria
        fields = ("sub_categoria_id", "sub_categoria_nombre", "sub_categoria_descripcion")

"""
//////////////////////////////////////////////////////
    Serializers relacionados con la RBS
//////////////////////////////////////////////////////
"""

class RbsSerializer(serializers.HyperlinkedModelSerializer):
    rbs_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Rbs
        fields = ("proyecto")


"""
//////////////////////////////////////////////////////
    Serializers relacionados con CategoriaRBS
//////////////////////////////////////////////////////
"""
class CategoriaRbsSerializer(serializers.ModelSerializer):
    categoria_rbs_id = serializers.IntegerField(read_only=True)
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = CategoriaRbs
        fields = ("categoria_rbs_id", "categoria", "rbs")


class CategoriaRbsSerializerInsert(serializers.ModelSerializer):
    categoria_rbs_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CategoriaRbs
        fields = ("categoria_rbs_id", "categoria", "rbs")

    def create(self, datos):
        categoriaRbs = CategoriaRbs(categoria=datos["categoria"], rbs=datos["rbs"])
        categoriaRbs.save()
        return categoriaRbs


"""
//////////////////////////////////////////////////////
    Serializers relacionados con SubCategoria RBS
//////////////////////////////////////////////////////
"""
class SubCategoriaRbsSerializer(serializers.ModelSerializer):
    sub_categoria_rbs_id = serializers.IntegerField(read_only=True)
    sub_categoria = SubCategoriaSerializer(read_only=True)
    class Meta:
        model = SubCategoriaRbs
        fields = ("sub_categoria_rbs_id", "sub_categoria", "categoria_rbs")


class SubCategoriaRbsSerializerInsert(serializers.ModelSerializer):
    sub_categoria_rbs_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SubCategoriaRbs
        fields = ("sub_categoria_rbs_id", "sub_categoria", "categoria_rbs")

    def create(self, datos):
        subCategoriaRbs = SubCategoriaRbs(categoria_rbs=datos["categoria_rbs"], sub_categoria=datos["sub_categoria"])
        subCategoriaRbs.save()
        return subCategoriaRbs




"""
//////////////////////////////////////////////////////
    Serializers relacionados con el modelo Proyecto
//////////////////////////////////////////////////////
"""
class ProyectoSerializer(serializers.ModelSerializer):
    proyecto_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Proyecto
        fields = ("proyecto_id",)


"""
//////////////////////////////////////////////////////
    Serializers relacionados con Responsable
//////////////////////////////////////////////////////
"""
class ResponsableSerializer(serializers.ModelSerializer):
    responsable_id = serializers.IntegerField(read_only=True)
    proyecto = ProyectoSerializer(read_only=True)
    class Meta:
        model = Responsable
        fields = ("responsable_id", "responsable_nombre", "responsable_descripcion", "proyecto")



class ResponsableSerializerList(serializers.HyperlinkedModelSerializer):
    responsable_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Responsable
        fields = ("responsable_id", "responsable_nombre", "responsable_descripcion",)


"""
//////////////////////////////////////////////////////
    Serializers relacionados con Riesgo
//////////////////////////////////////////////////////
"""
class RiesgoSerializer(serializers.HyperlinkedModelSerializer):
    riesgo_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Riesgo
        fields = ("riesgo_id", "riesgo_nombre", "riesgo_causa", "riesgo_evento", "riesgo_efecto", "riesgo_tipo", "riesgo_prom_evaluacion")

    def create(self, validated_data):
        sub_categoria_id = validated_data['sub_categoria_id']
        sub_categoria = SubCategoria.objects.get(sub_categoria_id = sub_categoria_id)
        validated_data['sub_categoria'] = sub_categoria
        riesgo = Riesgo.objects.create(**validated_data)
        return riesgo








#d
