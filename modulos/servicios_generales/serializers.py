from rest_framework import serializers, fields
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Gerente
from .models import Proyecto
from .models import Categoria

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

class ProyectoSerializerUpdate(serializers.HyperlinkedModelSerializer):
    proyecto_fecha_inicio = fields.DateField(input_formats=['%Y-%m-%d'])
    proyecto_fecha_finl = fields.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model = Proyecto
        fields = ("proyecto_objetivo", "proyecto_alcance", "proyecto_descripcion", "proyecto_presupuesto", "proyecto_fecha_inicio", "proyecto_fecha_finl", "gerente")







class SesionSerializer(serializers.HyperlinkedModelSerializer):  
    class Meta:
        model = Gerente
        fields = ("gerente_correo", "gerente_password")