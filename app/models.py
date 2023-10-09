from django.contrib.auth.models import AbstractUser
from django.db import models

class Roles(models.Model):
    ROLES_CHOICES = (
        ('Admin', 'Administrador'),
        ('F', 'Formulador'),
        ('E', 'Evaluador'),
        ('L', 'Lector'),
    )
    rol = models.CharField(max_length=20, choices=ROLES_CHOICES)

class Usuarios(AbstractUser):
    DOCUMENTS_CHOICES = (
        ('CC', 'Cedula de Ciudadania'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cedula de Extranjería'),
    )
    
    tipo_documento = models.CharField(max_length=20, choices=DOCUMENTS_CHOICES)
    num_documento = models.IntegerField()
    roles = models.ManyToManyField(Roles)

    def __str__(self):
        return self.username





class Proyecto(models.Model):
    titulo_Proyecto = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=200, null=False)
    codigo_Grupo_Investigacion = models.CharField(max_length=30, null=False)
    red_Conocimiento_Sectorial = models.CharField(max_length=100, null=False)
    disciplina_subarea = models.CharField(max_length=200, null=False)
    nombre_Grupo_Investigacion = models.CharField(max_length=100, null=False)
    area_conocimiento = models.CharField(max_length=80, null=False)
    linea_Grupo_Investigacion = models.CharField(max_length=100, null=False)
    subarea_conocimiento = models.CharField(max_length=100, null=False)
    # usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE) 

# Revisar
class Conocimientos(models.Model):
    areas_Conocimiento = models.CharField(max_length=100, null=False)
    subareas_Conocimiento = models.CharField(max_length=100, null=False)
    diciplinas_Subarea = models.CharField(max_length=100, null=False)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)

# Generalidades
class Informacion_Proyecto(models.Model):
    codigo_Dependencia_Presupuestal = models.CharField(max_length=50, null=False)
    tematicas_Estrategias_SENA = models.CharField(max_length=100, null=False)
    link_video_proyecto = models.CharField(max_length=500, null=False)
    proyecto_Relacionado_Industrial40 = models.BooleanField(null=False)
    justificacion_Industrial = models.CharField(max_length=500, null=True)
    actividades_economicas_del_proyecto_investigacion = models.CharField(max_length=100, null=False)
    proyecto_Relacionado_Economia_Naranja = models.BooleanField(null=False)
    justificacion_Economia_Naranja = models.CharField(max_length=500, null=True)
    proyecto_Relacionado_Politica_Discapacidad = models.BooleanField(null=False)
    justificacion_Politica_Discapacidad = models.CharField(max_length=500, null=True)
    # proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)

# class BaseRiesgo(models.Model):
#     tipo = models.CharField(max_length=50, null=False)
#     descripcion = models.CharField(max_length=150, null=False)
#     probabilidad = models.CharField(max_length=15, null=False)
#     impacto = models.CharField(max_length=150, null=False)
#     medidas_Mitigacion = models.CharField(max_length=150, null=False)
#     efectos = models.CharField(max_length=150, null=False)
#     # info_Proyecto = models.ForeignKey(Informacion_Proyecto, on_delete=models.CASCADE)

#     class Meta:
#         abstract = True

class RiesgoObjetivoGeneral(models.Model):
    tipo = models.CharField(max_length=50, null=False)
    descripcion = models.CharField(max_length=150, null=False)
    probabilidad = models.CharField(max_length=15, null=False)
    impacto = models.CharField(max_length=150, null=False)
    medidas_Mitigacion = models.CharField(max_length=150, null=False)
    efectos = models.CharField(max_length=150, null=False)
    # info_Proyecto = models.ForeignKey(Informacion_Proyecto, on_delete=models.CASCADE)

class RiesgoProductos(models.Model):
    tipo2 = models.CharField(max_length=50, null=False)
    descripcion2 = models.CharField(max_length=150, null=False)
    probabilidad2 = models.CharField(max_length=15, null=False)
    impacto2 = models.CharField(max_length=150, null=False)
    medidas_Mitigacion2 = models.CharField(max_length=150, null=False)
    efectos2 = models.CharField(max_length=150, null=False)
    # info_Proyecto = models.ForeignKey(Informacion_Proyecto, on_delete=models.CASCADE)

class RiesgoActividades(models.Model):
    tipo3 = models.CharField(max_length=50, null=False)
    descripcion3 = models.CharField(max_length=150, null=False)
    probabilidad3 = models.CharField(max_length=15, null=False)
    impacto3 = models.CharField(max_length=150, null=False)
    medidas_Mitigacion3 = models.CharField(max_length=150, null=False)
    efectos3 = models.CharField(max_length=150, null=False)
    # info_Proyecto = models.ForeignKey(Informacion_Proyecto, on_delete=models.CASCADE)
    
class Objetivos(models.Model):
    objetivo_general = models.CharField(max_length=250, null=False)
    informacion_proyecto = models.OneToOneField(Informacion_Proyecto, on_delete=models.CASCADE)

class Objetivos_especificos(models.Model):
    objetivo_especificos = models.CharField(max_length=250, null=False)
    objetivos = models.ForeignKey(Objetivos, on_delete=models.CASCADE)

class Actividades_de_objetivos_especificos(models.Model):
    actividades_obj_especificos = models.CharField(max_length=250, null=False)
    objetivos_especificos = models.ForeignKey(Objetivos_especificos, on_delete=models.CASCADE)

class Estructura_del_proyecto(models.Model):
    resumen_ejecutivo = models.CharField(max_length=250, null=False)
    antecedentes = models.CharField(max_length=250, null=False)
    # informacion_proyecto = models.OneToOneField(Informacion_Proyecto, on_delete=models.CASCADE)

class Estructura_arbol_problemas(models.Model):
    arbol_de_problemas = models.CharField(max_length=150, null=True)

class Estructura_problema(models.Model):
    identificacion_y_descripcion_problema = models.CharField(max_length=250, null=False)
    justificacion = models.CharField(max_length=250, null=False)
    # marco_conceptual = models.ImageField()

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
    informacion_proyecto = models.ForeignKey(Informacion_Proyecto, on_delete=models.CASCADE)

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
    descripcion_recursos_especie_aportados = models.CharField(max_length=150, null=True)
    recursos_dinero_entidad_aliada = models.BigIntegerField(null=True)
    descripcion_destinacion_dinero_aportado = models.CharField(max_length=150, null=True)
    nombre_grupo_inv_entidad_aliada = models.CharField(max_length=170, null=True)
    codigo_gruplac_entidad_aliada = models.CharField(max_length=50, null=True)
    link_gruplac_entidad_aliada = models.CharField(max_length=500 ,null=True)
    actividades_desarrollar_entidad_aliada_marco_proyecto = models.CharField(max_length=250, null=True)
    objetivo_especificos_relacionados = models.CharField(max_length=250, null=True)
    metodologia_act_transferencia_centro_formacion = models.CharField(max_length= 250, null=True)
    # informacion_proyecto = models.ForeignKey(Informacion_Proyecto, on_delete=models.CASCADE)

# Informacion proponente
class Informacion_de_centro(models.Model):
    Region = models.CharField(max_length=50, null=False)
    Regional = models.CharField(max_length=50, null=False)
    Nombre_centro_formacion = models.CharField(max_length=100, null=False)
    Nombre_Director = models.CharField(max_length=50, null=False)
    Numero_Director = models.BigIntegerField(null=False)
    email_director = models.CharField(max_length=100, null=False)
    Nombre_Sub_Director = models.CharField(max_length=50, null=False)
    Numero_Sub_Director = models.BigIntegerField(null=False)
    email_sub_director = models.CharField(max_length=100, null=False)

    # Info_Proyecto = models.OneToOneField(Informacion_Proyecto, on_delete=models.CASCADE)
    
class Participantes_Proyecto(models.Model):
    Nombre_participantes_de_desarrollo = models.CharField(max_length=50, null=True)
    Rol_Sennova_De_Participantes_de_Proyecto = models.CharField(max_length=50, choices=[('formulador', 'Formulador'), ('investigador', 'Investigador'), ('dinamizador', 'Dinamizador'), ('instructor', 'Instructor'), ('aprendiz','Aprendiz')], null=True)
    Numero_cedula_participantes = models.IntegerField(null=True)
    Numero_meses_vinculacion_participantes = models.IntegerField(null=False)
    Email_participantes_de_desarrollo = models.EmailField(null=True)
    Numero_horas_Semanales_dedicadas_participantes = models.IntegerField(null=False)
    Numero_Telefono_participantes = models.BigIntegerField(null=True)
    # Info_Proyecto = models.ForeignKey(Informacion_Proyecto, on_delete=models.CASCADE)
    
class Autores(models.Model):
    Nombre_Autor_Proyecto = models.CharField(null=False, max_length=50)
    Tipo_Vinculacion_entidad = models.CharField(max_length=15 ,null=False, choices=[('planta', 'Planta'), ('contratista', 'Contratista') , ('planta_temporal' , 'Planta_temporal')])
    Numero_Cedula_Autor = models.IntegerField(null=False)
    Rol_Sennova_De_Participantes_de_Proyecto = models.CharField(max_length=50, choices=[('formulador', 'Formulador'), ('investigador', 'Investigador'), ('dinamizador', 'Dinamizador'), ('instructor', 'Instructor'), ('aprendiz','Aprendiz')], null=True)
    Email_Autor_Proyecto = models.EmailField(null=False)
    Numero_meses_vinculacion_Autor = models.IntegerField(null=False)
    Numero_Telefono_Autor = models.BigIntegerField(null=False)
    Numero_horas_Semanales_dedicadas_Autores = models.IntegerField(null=False)
    # Info_Proyecto = models.ForeignKey(Informacion_Proyecto, on_delete=models.CASCADE)

# Centro de formacion
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
    # Info_Proyecto = models.ForeignKey(Informacion_Proyecto, on_delete=models.CASCADE)