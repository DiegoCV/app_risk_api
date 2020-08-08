from rest_framework import serializers, fields

from .models import Rbs
from .models import Proyecto
from .models import Categoria
from .models import SubCategoria
from .models import CategoriaRbs
from .models import SubCategoriaRbs


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







#d
