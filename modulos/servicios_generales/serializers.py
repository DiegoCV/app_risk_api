from rest_framework import serializers, fields
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Gerente
from .models import Proyecto
from .models import Categoria
from .models import SubCategoria
from .models import Riesgo
from .models import Respuesta
from .models import AccionRespuesta
from .models import RespuestaHasRiesgo
from .models import TipoRecurso
from .models import Recurso

"""
//////////////////////////////////////////////////////
    Serializers relacionados con los tokens
//////////////////////////////////////////////////////
"""
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['gerente_id'] = user.id
        return token

class SesionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gerente
        fields = ("gerente_correo", "gerente_password")
"""
//////////////////////////////////////////////////////
    Serializers relacionados con el modelo Gerente
//////////////////////////////////////////////////////
"""
class GerenteSerializer(serializers.HyperlinkedModelSerializer):
    gerente_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Gerente
        fields = ("gerente_id", "gerente_nombre", "gerente_usuario", "gerente_correo", "gerente_password", "gerente_fecha_creacion")

class GerenteSerializerUtil(serializers.HyperlinkedModelSerializer):
    gerente_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Gerente
        fields = ("gerente_id", "gerente_nombre", "gerente_usuario", "gerente_correo", "gerente_password", "gerente_fecha_creacion")

"""
//////////////////////////////////////////////////////
    Serializers relacionados con el modelo Proyecto
//////////////////////////////////////////////////////
"""
class ProyectoSerializer(serializers.HyperlinkedModelSerializer):
    proyecto_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Proyecto
        fields = ("proyecto_id", "proyecto_nombre", "proyecto_objetivo", "proyecto_alcance", "proyecto_descripcion", "proyecto_presupuesto", "proyecto_fecha_inicio", "proyecto_fecha_finl", "proyecto_evaluacion_general", "proyecto_evaluacion")

class ProyectoSerializerInsert(serializers.HyperlinkedModelSerializer):
    proyecto_fecha_inicio = fields.DateField(input_formats=['%Y-%m-%d'])
    proyecto_fecha_finl = fields.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model = Proyecto
        fields = ("proyecto_nombre", "proyecto_objetivo", "proyecto_alcance", "proyecto_descripcion", "proyecto_presupuesto", "proyecto_fecha_inicio", "proyecto_fecha_finl", "proyecto_evaluacion_general", "proyecto_evaluacion")
    def create(self, validated_data, gerente_usuario):
        gerente = Gerente.objects.get(gerente_usuario = gerente_usuario )
        validated_data['gerente'] = gerente
        Proyecto.objects.create(**validated_data)

class ProyectoSerializerInsert_2(serializers.HyperlinkedModelSerializer):
    proyecto_fecha_inicio = fields.DateField(input_formats=['%Y-%m-%d'])
    #proyecto_fecha_finl = fields.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model = Proyecto
        fields = ("proyecto_nombre", "proyecto_objetivo", "proyecto_alcance", "proyecto_descripcion", "proyecto_presupuesto", "proyecto_fecha_inicio", "proyecto_evaluacion_general", "proyecto_evaluacion")
    def create(self, validated_data, gerente_usuario):
        gerente = Gerente.objects.get(gerente_usuario = gerente_usuario )
        validated_data['gerente'] = gerente
        Proyecto.objects.create(**validated_data)

class ProyectoSerializerUpdate(serializers.HyperlinkedModelSerializer):
    proyecto_fecha_inicio = fields.DateField(input_formats=['%Y-%m-%d'])
    proyecto_fecha_finl = fields.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model = Proyecto
        fields = ("proyecto_objetivo", "proyecto_alcance", "proyecto_descripcion", "proyecto_presupuesto", "proyecto_fecha_inicio", "proyecto_fecha_finl", "gerente")

"""
//////////////////////////////////////////////////////
    Serializers relacionados con el modelo de Categoria
//////////////////////////////////////////////////////
"""
class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    categoria_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Categoria
        fields = ("categoria_id", "categoria_nombre", "categoria_descripcion")

    def create(self, validated_data, gerente_id):
        gerente = Gerente.objects.get(gerente_id = gerente_id)
        validated_data['gerente'] = gerente
        Categoria.objects.create(**validated_data)


"""
//////////////////////////////////////////////////////
    Serializers relacionados con el modelo de SubCategoria
//////////////////////////////////////////////////////
"""
class SubCategoriaSerializer(serializers.HyperlinkedModelSerializer):
    sub_categoria_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = SubCategoria
        fields = ("sub_categoria_id", "sub_categoria_nombre", "sub_categoria_descripcion")



    def create(self, validated_data):
        categoria_id = validated_data['categoria_id']
        categoria = Categoria.objects.get(categoria_id = categoria_id)
        validated_data['categoria'] = categoria
        SubCategoria.objects.create(**validated_data)


class SubCategoriaSerializerUpdate(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCategoria
        fields = ("sub_categoria_nombre", "sub_categoria_descripcion")

"""
//////////////////////////////////////////////////////
    Serializers relacionados con el modelo de Riesgo
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
        Riesgo.objects.create(**validated_data)


class RiesgoSerializerUpdate(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Riesgo
        fields = ("riesgo_nombre", "riesgo_causa", "riesgo_evento", "riesgo_efecto", "riesgo_tipo", "riesgo_prom_evaluacion")


"""
//////////////////////////////////////////////////////
    Serializers relacionados con el modelo de Respuesta
//////////////////////////////////////////////////////
"""
class RespuestaSerializer(serializers.HyperlinkedModelSerializer):
    respuesta_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Respuesta
        fields = ("respuesta_id", "respuesta_nombre", "respuesta_descripcion", "respuesta_costo")

    def create(self, validated_data, gerente_id):
        gerente = Gerente.objects.get(gerente_id = gerente_id)
        validated_data['gerente_gerente'] = gerente
        respuesta = Respuesta.objects.create(**validated_data)
        return respuesta


class RespuestaSerializerInsert(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Respuesta
        fields = ("respuesta_nombre", "respuesta_descripcion", "respuesta_costo")

    def create(self, validated_data, gerente_id):
        gerente = Gerente.objects.get(gerente_id = gerente_id)
        validated_data['gerente_gerente'] = gerente
        respuesta = Respuesta.objects.create(**validated_data)
        return respuesta

"""
//////////////////////////////////////////////////////
    Serializers relacionados con el modelo de AccionRespuesta
//////////////////////////////////////////////////////
"""
class AccionRespuestaSerializer(serializers.HyperlinkedModelSerializer):
    accion_respuesta_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = AccionRespuesta
        fields = ("accion_respuesta_id", "accion_respuesta_descripcion")


"""
//////////////////////////////////////////////////////
    Serializers relacionados con el modelo de TipoRecurso
//////////////////////////////////////////////////////
"""

class TipoRecursoSerializer(serializers.HyperlinkedModelSerializer):
    tipo_recurso_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = TipoRecurso
        fields = ("tipo_recurso_id", "tipo_recurso_nombre", "tipo_recurso_descripcion")

    def create(self, validated_data, gerente_id):
        gerente = Gerente.objects.get(gerente_id = gerente_id)
        validated_data['gerente'] = gerente
        respuesta = TipoRecurso.objects.create(**validated_data)
        return respuesta

class TipoRecursoSerializerInsert(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TipoRecurso
        fields = ("tipo_recurso_nombre", "tipo_recurso_descripcion")


"""
//////////////////////////////////////////////////////
    Serializers relacionados con el modelo de Recurso
//////////////////////////////////////////////////////
"""
class RecursoSerializer(serializers.HyperlinkedModelSerializer):
    recurso_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Recurso
        fields = ("recurso_id", "recurso_nombre", "recurso_costo",)

    def create(self, validated_data, gerente_id, tipo_recurso_id):
        gerente = Gerente.objects.get(gerente_id = gerente_id)
        tipo_recurso = TipoRecurso.objects.get(tipo_recurso_id = tipo_recurso_id)
        validated_data['gerente'] = gerente
        validated_data['tipo_recurso'] = tipo_recurso
        respuesta = Recurso.objects.create(**validated_data)
        return respuesta
