# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccionRespuesta(models.Model):
    accion_respuesta_id = models.AutoField(primary_key=True)
    accion_respuesta_descripcion = models.CharField(max_length=45, blank=True, null=True)
    respuesta = models.ForeignKey('Respuesta', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accion_respuesta'


class Actividad(models.Model):
    actividad_id = models.AutoField(primary_key=True)
    actividad_nombre = models.CharField(max_length=100, blank=True, null=True)
    actividad_fecha_inicio = models.DateField(blank=True, null=True)
    actividad_fecha_fin = models.DateField(blank=True, null=True)
    proyecto = models.ForeignKey('Proyecto', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'actividad'


class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    categoria_nombre = models.CharField(max_length=45, blank=True, null=True)
    categoria_descripcion = models.TextField(blank=True, null=True)
    gerente = models.ForeignKey('Gerente', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'categoria'


class CategoriaRbs(models.Model):
    categoria_rbs_id = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING)
    rbs = models.ForeignKey('Rbs', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'categoria_rbs'
        unique_together = (('categoria', 'rbs'),)


class Gerente(models.Model):
    gerente_id = models.AutoField(primary_key=True)
    gerente_nombre = models.CharField(max_length=100, blank=True, null=True)
    gerente_usuario = models.CharField(unique=True, max_length=45)
    gerente_correo = models.CharField(max_length=100, blank=True, null=True)
    gerente_password = models.CharField(max_length=100, blank=True, null=True)
    gerente_fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'gerente'


class Proyecto(models.Model):
    proyecto_id = models.AutoField(primary_key=True)
    proyecto_nombre = models.CharField(max_length=100)
    proyecto_objetivo = models.TextField(blank=True, null=True)
    proyecto_alcance = models.TextField(blank=True, null=True)
    proyecto_descripcion = models.TextField(blank=True, null=True)
    proyecto_presupuesto = models.FloatField(blank=True, null=True)
    proyecto_fecha_inicio = models.DateField(blank=True, null=True)
    proyecto_fecha_finl = models.DateField(blank=True, null=True)
    proyecto_evaluacion_general = models.TextField(blank=True, null=True)
    proyecto_evaluacion = models.IntegerField(blank=True, null=True)
    gerente = models.ForeignKey(Gerente, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'proyecto'


class Rbs(models.Model):
    rbs_id = models.AutoField(primary_key=True)
    proyecto = models.OneToOneField(Proyecto, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'rbs'


class Recurso(models.Model):
    recurso_id = models.AutoField(primary_key=True)
    recurso_nombre = models.CharField(max_length=45, blank=True, null=True)
    recurso_costo = models.FloatField(blank=True, null=True)
    tipo_recurso = models.ForeignKey('TipoRecurso', models.DO_NOTHING)
    gerente = models.ForeignKey(Gerente, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recurso'


class Responsable(models.Model):
    responsable_id = models.AutoField(primary_key=True)
    responsable_nombre = models.CharField(max_length=100)
    responsable_descripcion = models.TextField(blank=True, null=True)
    proyecto = models.ForeignKey(Proyecto, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'responsable'


class Respuesta(models.Model):
    respuesta_id = models.AutoField(primary_key=True)
    respuesta_nombre = models.CharField(max_length=45, blank=True, null=True)
    respuesta_descripcion = models.TextField(blank=True, null=True)
    respuesta_costo = models.FloatField(blank=True, null=True)
    gerente_gerente = models.ForeignKey(Gerente, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'respuesta'


class RespuestaHasRiesgo(models.Model):
    respuesta = models.OneToOneField(Respuesta, models.DO_NOTHING)
    riesgo = models.OneToOneField('Riesgo', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'respuesta_has_riesgo'


class RespuestaRbs(models.Model):
    respuesta_rbs_id = models.AutoField(primary_key=True)
    respuesta = models.ForeignKey(Respuesta, models.DO_NOTHING)
    rbs = models.ForeignKey(Rbs, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'respuesta_rbs'
        unique_together = (('respuesta', 'rbs'),)


class Riesgo(models.Model):
    riesgo_id = models.AutoField(primary_key=True)
    riesgo_nombre = models.CharField(max_length=45, blank=True, null=True)
    riesgo_causa = models.TextField(blank=True, null=True)
    riesgo_evento = models.TextField(blank=True, null=True)
    riesgo_efecto = models.TextField(blank=True, null=True)
    riesgo_tipo = models.IntegerField(blank=True, null=True)
    riesgo_prom_evaluacion = models.FloatField(blank=True, null=True)
    sub_categoria = models.ForeignKey('SubCategoria', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'riesgo'


class RiesgoRbs(models.Model):
    riesgo_rbs_id = models.AutoField(primary_key=True)
    sub_categoria_rbs = models.ForeignKey('SubCategoriaRbs', models.DO_NOTHING)
    riesgo = models.ForeignKey(Riesgo, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'riesgo_rbs'
        unique_together = (('riesgo_rbs_id', 'sub_categoria_rbs', 'riesgo'),)


class RiesgoRbsHasRespuestaRbs(models.Model):
    riesgo_rbs_riesgo_rbs = models.OneToOneField(RiesgoRbs, models.DO_NOTHING, primary_key=True)
    respuesta_rbs_respuesta_rbs = models.ForeignKey(RespuestaRbs, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'riesgo_rbs_has_respuesta_rbs'
        unique_together = (('riesgo_rbs_riesgo_rbs', 'respuesta_rbs_respuesta_rbs'),)


class SubCategoria(models.Model):
    sub_categoria_id = models.AutoField(primary_key=True)
    sub_categoria_nombre = models.CharField(max_length=45, blank=True, null=True)
    sub_categoria_descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sub_categoria'


class SubCategoriaRbs(models.Model):
    sub_categoria_rbs_id = models.AutoField(primary_key=True)
    sub_categoria = models.ForeignKey(SubCategoria, models.DO_NOTHING)
    categoria_rbs = models.ForeignKey(CategoriaRbs, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sub_categoria_rbs'


class TipoRecurso(models.Model):
    tipo_recurso_id = models.AutoField(primary_key=True)
    gerente = models.ForeignKey(Gerente, models.DO_NOTHING)
    tipo_recurso_nombre = models.CharField(max_length=45)
    tipo_recurso_descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_recurso'
