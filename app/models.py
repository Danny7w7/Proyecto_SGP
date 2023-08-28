from django.db import models

# Create your models here.
class Objetivos(models.Model):
    objetivo_general = models.CharField(max_length=250, null=False)

class Objetivos_especificos(models.Model):
    objetivo_especificos = models.CharField(max_length=250, null=False)

class Actividades_de_objetivos_especificos(models.Model):
    Actividades_obj_especificos = models.CharField(max_length=250, null=False)

class Estructura_del_proyecto(models.Model):
    resumen_ejecutivo = models.CharField(max_length=250, null=False)
    antecedentes = models.CharField(max_length=250, null=False)
    # arbol_de_problemas = models.CharField()
    identificacion_y_descripcion_problema = models.CharField(max_length=250, null=False)
    justificacion = models.CharField(max_length=250, null=False)
    marco_conceptual = models.CharField(max_length=250, null=False)

class Resultados_y_productos_esperados(models.Model):
    tipo_resultado_esperado_obj_especifico = models.CharField(max_length=250, null=False)
    descripcion_resultado_esperado_obj_especifico = models.CharField(max_length=250, null=False)
    nombre_producto_resultado_inv_obj_especifico = models.CharField(max_length=100, null=False)
    trl_producto_resultado_inv_obj_especifico = models.CharField(max_length=100, null=False)
    indicador_producto_resultado_inv_obj_especifico = models.CharField(max_length=50, null=False)
    fch_entrega_producto_resultado_inv_obj_especifico = models.DateTimeField(null=False)
    duracion = models.DurationField(null=False)
    fch_inicio = models.DateTimeField(null=False)
    fch_cierre = models.DateTimeField(null=False)
    cadena_valor = models.ImageField(null=False)
    propuesta_sostenibilidad = models.CharField(max_length=150, null=False)
    impacto_social= models.CharField(max_length=150, null=False)
    impacto_tecnologico = models.CharField(max_length= 150, null=False)
    impacto_centro_formacion = models.CharField(max_length=150, null=False)

class Entidades_aliadas(models.Model):
    nombre_entidad = models.CharField(max_length=170, null=True)
    tipo_entidad_aliada = models.CharField(max_length=50, null=True)
    naturaleza_entidad = models.CharField(max_length=50, null=True)
    clasificiacion_empresa = models.CharField(max_length=50, null=True)
    nit = models.BigIntegerField(null=True)
    convenio = models.BooleanField(null=True)
    especifique_tipo_codigo_convenio = models.CharField(max_length=150, null=True)
    nombres_integrantes_participantes_entidad_aliada = models.CharField(max_length=150, null=True)
    numero_identificacion_integrantes = models.BigIntegerField(null=True)
    email_integrantes = models.EmailField(null=True)
    numeros_celular_integrantes = models.BigIntegerField(null=True)
    recursos_especie_entidad = models.BigIntegerField(null=True)
    descripcion_recursos_especie_aportados = models.BigIntegerField(null=True)
    recursos_dinero_entidad_aliada = models.BigIntegerField(null=True)
    descripcion_destinacion_dinero_aportado = models.CharField(max_length=150, null=True)
    nombre_grupo_inv_entidad_aliada = models.CharField(max_length=170, null=True)
    codigo_gruplac_entidad_aliada = models.IntegerField(null=True)
    link_gruplac_entidad_aliada = models.CharField(null=True)
    actividades_desarrollar_entidad_aliada_marco_proyecto = models.CharField(max_length=250, null=True)
    objetivo_especificos_relacionados = models.CharField(max_length=250, null=True)
    metodologia_act_transferencia_centro_formacion = models.CharField(max_length= 250, null=True)
