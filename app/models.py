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
    
    temp_password = models.CharField(max_length=8)
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
    progress = models.IntegerField(null=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

# Informacion del Proyecto
class Informacion_proponente(models.Model):
    Region = models.CharField(max_length=50, null=True)
    Regional = models.CharField(max_length=50, null=True)
    Nombre_centro_formacion = models.CharField(max_length=100, null=True)
    Nombre_Director = models.CharField(max_length=50, null=True)
    Numero_Director = models.BigIntegerField(null=True)
    email_director = models.CharField(max_length=100, null=True)
    Nombre_Sub_Director = models.CharField(max_length=50, null=True)
    Numero_Sub_Director = models.BigIntegerField(null=True)
    email_sub_director = models.CharField(max_length=100, null=True)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)
    
class Autores(models.Model):
    nombre_Autor_Proyecto = models.CharField(null=True, max_length=50)
    tipo_Vinculacion_entidad = models.CharField(max_length=15 ,null=True, choices=[('planta', 'Planta'), ('contratista', 'Contratista') , ('planta_temporal' , 'Planta_temporal')])
    numero_Cedula_Autor = models.IntegerField(null=True)
    rol_Sennova_De_Participantes_de_Proyecto = models.CharField(max_length=50, choices=[('formulador', 'Formulador'), ('investigador', 'Investigador'), ('dinamizador', 'Dinamizador'), ('instructor', 'Instructor'), ('aprendiz','Aprendiz')], null=True)
    email_Autor_Proyecto = models.EmailField(null=True)
    numero_meses_vinculacion_Autor = models.IntegerField(null=True)
    numero_Telefono_Autor = models.BigIntegerField(null=True)
    numero_horas_Semanales_dedicadas_Autores = models.IntegerField(null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    
class Participantes_Proyecto(models.Model):
    nombre_participantes_de_desarrollo = models.CharField(max_length=50, null=True)
    rol_Sennova_De_Participantes_de_Proyecto = models.CharField(max_length=50, choices=[('formulador', 'Formulador'), ('investigador', 'Investigador'), ('dinamizador', 'Dinamizador'), ('instructor', 'Instructor'), ('aprendiz','Aprendiz')], null=True)
    numero_cedula_participantes = models.IntegerField(null=True)
    numero_meses_vinculacion_participantes = models.IntegerField(null=True)
    email_participantes_de_desarrollo = models.EmailField(null=True)
    numero_horas_Semanales_dedicadas_participantes = models.IntegerField(null=True)
    numero_Telefono_participantes = models.BigIntegerField(null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

class Generalidades_del_proyecto(models.Model):
    codigo_Dependencia_Presupuestal = models.CharField(max_length=50, null=True)
    tematicas_Estrategias_SENA = models.CharField(max_length=100, null=True)
    link_video_proyecto = models.CharField(max_length=500, null=True)
    proyecto_Relacionado_Industrial40 = models.BooleanField(null=True)
    justificacion_Industrial = models.CharField(max_length=500, null=True)
    actividades_economicas_del_proyecto_investigacion = models.CharField(max_length=100, null=True)
    proyecto_Relacionado_Economia_Naranja = models.BooleanField(null=True)
    justificacion_Economia_Naranja = models.CharField(max_length=500, null=True)
    proyecto_Relacionado_Politica_Discapacidad = models.BooleanField(null=True)
    justificacion_Politica_Discapacidad = models.CharField(max_length=500, null=True)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)


#Estructura del proyecto
class Resumen_antecedentes(models.Model):
    resumen_ejecutivo = models.CharField(max_length=250, null=True)
    antecedentes = models.CharField(max_length=250, null=True)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)

class Arbol_problemas(models.Model):
    arbol_de_problemas = models.CharField(max_length=150, null=True)

class Descripcion_problema(models.Model):
    identificacion_y_descripcion_problema = models.CharField(max_length=250, null=False)
    justificacion = models.CharField(max_length=250, null=False)
    marco_conceptual = models.ImageField(upload_to='')
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)


# Objetivos
class Objetivos(models.Model):
    objetivo_general = models.CharField(max_length=250, null=True)
    objetivo_proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)
    # informacion_proyecto = models.OneToOneField(Informacion_Proyecto, on_delete=models.CASCADE)

# Metodologia
class Objetivos_especificos(models.Model):
    objetivo_especificos = models.CharField(max_length=250, null=True)
    objetivos = models.ForeignKey(Objetivos, on_delete=models.CASCADE)

class Actividades_de_objetivos_especificos(models.Model):
    actividades_obj_especificos = models.CharField(max_length=250, null=False)
    objetivos_especificos = models.OneToOneField(Objetivos_especificos, on_delete=models.CASCADE)

class Causa(models.Model):
    causa = models.CharField(max_length=200, null=True)
    obejetivo_especifico = models.OneToOneField(Objetivos_especificos, on_delete=models.CASCADE)
    
class Efecto(models.Model):
    efecto = models.CharField(max_length=200, null=True)
    causas = models.OneToOneField(Causa, on_delete=models.CASCADE)

# Analisis de participantes
class Centro_de_formacion(models.Model):
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


# Resultados y productos esperados
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
    # informacion_proyecto = models.ForeignKey(Informacion_Proyecto, on_delete=models.CASCADE)


#Riesgos
class BaseRiesgo(models.Model):
    tipo = models.CharField(max_length=50, null=True)
    descripcion = models.CharField(max_length=150, null=True)
    probabilidad = models.CharField(max_length=15, null=True)
    impacto = models.CharField(max_length=150, null=True)
    medidas_Mitigacion = models.CharField(max_length=150, null=True)
    efectos = models.CharField(max_length=150, null=True)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class RiesgoObjetivoGeneral(BaseRiesgo):
    pass

class RiesgoProductos(BaseRiesgo):
    pass

class RiesgoActividades(BaseRiesgo):
    pass

class Document(models.Model):
    anexo1 = models.ImageField(upload_to="", null=True)
    anexo2 = models.ImageField(upload_to="", null=True)
    anexo3 = models.ImageField(upload_to="", null=True)
    anexo4 = models.ImageField(upload_to="", null=True)
    anexo5 = models.ImageField(upload_to="", null=True)
    anexo6 = models.ImageField(upload_to="", null=True)
    fecha = models.DateTimeField(auto_now=True)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)


# Listas plegable
class Listas_plegables(models.Model):
    codigos_grupo_investigacion = models.CharField(max_length=10, null=True)
    nombre_grupo_investigacion = models.CharField(max_length=200, null=True)
    redes_conocimiento = models.CharField(max_length=200, null=True)
    subareas_conocimiento = models.CharField(max_length=200, null=True)
    diciplina_subarea = models.CharField(max_length=200, null=True)
    nombre_centro_formacion = models.CharField(max_length=200, null=True)
    
#Middleware
class UltimaVista(models.Model):
    usuario = models.OneToOneField(Usuarios, on_delete=models.CASCADE)
    ultima_vista = models.CharField(max_length=255, null=True)