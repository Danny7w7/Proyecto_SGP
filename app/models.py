from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Roles(models.Model):
    administrador = models.BooleanField()
    formulador = models.BooleanField()
    evaluador = models.BooleanField()
    lector = models.BooleanField()

class Usuarios(AbstractUser):
    cc_nit = models.IntegerField()
    roles = models.ManyToManyField(Roles)

    def __str__(self):
        return self.username

class Proyecto(models.Model):
    codigo_Grupo_Investigacion = models.IntegerField(null=False)
    nombre_Grupo_Investigacion = models.CharField(max_length=100, null=False)
    linea_Grupo_Investigacion = models.CharField(max_length=100, null=False)
    titulo_Proyecto = models.CharField(max_length=100, null=False)
    red_Conocimiento_Sectorial = models.CharField(max_length=100, null=False)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE) 

class Conocimientos(models.Model):
    areas_Conocimiento = models.CharField(max_length=100, null=False)
    subareas_Conocimiento = models.CharField(max_length=100, null=False)
    diciplinas_Subarea = models.CharField(max_length=100, null=False)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)

class Informacion_Proyecto(models.Model):
    codigo_Dependencia_Presupuestal = models.CharField(max_length=10, null=False)
    actividades_economicas_del_proyecto_investigacion = models.CharField(max_length=100, null=False)
    tematicas_Estrategias_SENA = models.CharField(max_length=100, null=False)
    link_video_proyecto = models.CharField(max_length=500, null=False)
    proyecto_Relacionado_Industrial40 = models.BooleanField(null=False)
    justificacion_Industrial = models.CharField(max_length=500, null=True)
    proyecto_Relacionado_Economia_Naranja = models.BooleanField(null=False)
    justificacion_Economia_Naranja = models.CharField(max_length=500, null=True)
    proyecto_Relacionado_Politica_Discapacidad = models.BooleanField(null=False)
    justificacion_Politica_Discapacidad = models.CharField(max_length=500, null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE) 

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
    link_gruplac_entidad_aliada = models.CharField(max_length=500 ,null=True)
    actividades_desarrollar_entidad_aliada_marco_proyecto = models.CharField(max_length=250, null=True)
    objetivo_especificos_relacionados = models.CharField(max_length=250, null=True)
    metodologia_act_transferencia_centro_formacion = models.CharField(max_length= 250, null=True)

class Informacion_de_centro(models.Model):
    Region = models.CharField(max_length=50, null=False)
    Regional = models.CharField(max_length=50, null=False)
    Nombre_centro_formacion = models.CharField(max_length=100, null=False)
    Nombre_Director = models.CharField(max_length=50, null=False)
    Numero_Director = models.IntegerField(null=False)
    Nombre_Sub_Director = models.CharField(max_length=50, null=False)
    Numero_Sub_Director = models.IntegerField(null=False)
    
class Participantes_Proyecto(models.Model):
    Nombre_participantes_de_desarrollo = models.CharField(max_length=50, null=True)
    Numero_cedula_participantes = models.IntegerField(null=True)
    Email_participantes_de_desarrollo = models.EmailField(null=True)
    Numero_Telefono_participantes = models.IntegerField(null=True)
    Rol_Sennova_De_Participantes_de_Proyecto = models.CharField(max_length=50, choices=[('formulador', 'Formulador'), ('investigador', 'Investigador'), ('dinamizador', 'Dinamizador'), ('instructor', 'Instructor'), ('aprendiz','Aprendiz')], null=True)
    Numero_meses_vinculacion_participantes = models.IntegerField(null=False)
    Numero_horas_Semanales_dedicadas_participantes = models.IntegerField(null=False)
    
class Autores(models.Model):
    Nombre_Autor_Proyecto = models.CharField(null=False, max_length=50)
    Numero_Cedula_Autor = models.IntegerField(null=False)
    Email_Autor_Proyecto = models.EmailField(null=False)
    Numero_Telefono_Autor = models.IntegerField(null=False)
    Tipo_Vinculacion_entidad = models.CharField(max_length=15 ,null=False, choices=[('planta', 'Planta'), ('contratista', 'Contratista') , ('planta_temporal' , 'Planta_temporal')])
    Rol_Sennova_De_Participantes_de_Proyecto = models.CharField(max_length=50, choices=[('formulador', 'Formulador'), ('investigador', 'Investigador'), ('dinamizador', 'Dinamizador'), ('instructor', 'Instructor'), ('aprendiz','Aprendiz')], null=True)
    Numero_meses_vinculacion_Autor = models.IntegerField(null=False)
    Numero_horas_Semanales_dedicadas_Autores = models.IntegerField(null=False)
    
class Analisis_Participantes(models.Model):
    Nombre_Semillero_Investigacion_Beneficiados = models.CharField(null=False, max_length=100)
    Numero_Programas_Beneficiarios_Semilleros_Investigacion = models.IntegerField(null=False)
    Tipo_programas_formación_beneficiados_conforman_semillero = models.CharField(null=False, max_length=100)
    Nombre_programas_formación_beneficiados_semillero = models.CharField(null=False, max_length=100)
    Tipo_programas_de_formación_beneficiados_por_ejecución = models.CharField(null=True, max_length=100)
    Nombre_programas_formación_beneficiados_ejecución_proyecto = models.CharField(null=True, max_length=100)
    Número_aprendices_participarán_ejecución_proyecto = models.IntegerField(null=False)
    Número_municipios_beneficiados = models.IntegerField(null=False)
    Nombre_municipios_beneficiados_descripción_beneficio = models.CharField(null=False, max_length=200)