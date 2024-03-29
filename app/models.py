from django.contrib.auth.models import AbstractUser
from django.db import models

from unidecode import unidecode
import re

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
    num_documento = models.BigIntegerField()
    roles = models.ManyToManyField(Roles)

    def __str__(self):
        return self.username

class Proyecto(models.Model):
    titulo_Proyecto = models.CharField(max_length=500, null=False)
    descripcion = models.CharField(max_length=5000, null=False)
    codigo_Grupo_Investigacion = models.CharField(max_length=30, null=False)
    red_Conocimiento_Sectorial = models.CharField(max_length=100, null=False)
    disciplina_subarea = models.CharField(max_length=200, null=False)
    nombre_Grupo_Investigacion = models.CharField(max_length=150, null=False)
    area_conocimiento = models.CharField(max_length=80, null=False)
    linea_Grupo_Investigacion = models.CharField(max_length=100, null=False)
    subarea_conocimiento = models.CharField(max_length=100, null=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    progress = models.IntegerField(null=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

class Estado(models.Model):
    STATE_CHOICES = (
        ('1', 'Terminados'),
        ('2', 'Pendientes'),
        ('3', 'Suspendido'),
    )
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)

# Informacion del Proyecto
class Informacion_proponente(models.Model):
    Region = models.CharField(max_length=50, null=True)
    Regional = models.CharField(max_length=50, null=True)
    Nombre_centro_formacion = models.CharField(max_length=100, null=True)
    Nombre_Director = models.CharField(max_length=40, null=True)
    Numero_Director = models.CharField(max_length=30,  null=True)
    email_director = models.CharField(max_length=40, null=True)
    Nombre_Sub_Director = models.CharField(max_length=40, null=True)
    Numero_Sub_Director = models.CharField(max_length=30, null=True)
    email_sub_director = models.CharField(max_length=40, null=True)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)
    
class Autores(models.Model):
    nombre_Autor_Proyecto = models.CharField(null=True, max_length=40)
    tipo_Vinculacion_entidad = models.CharField(max_length=15 ,null=True, choices=[('planta', 'Planta'), ('contratista', 'Contratista') , ('planta_temporal' , 'Planta_temporal')])
    numero_Cedula_Autor = models.BigIntegerField(null=True)
    rol_Sennova_De_Participantes_de_Proyecto = models.CharField(max_length=50, choices=[('formulador', 'Formulador'), ('investigador', 'Investigador'), ('dinamizador', 'Dinamizador'), ('instructor', 'Instructor'), ('aprendiz','Aprendiz')], null=True)
    email_Autor_Proyecto = models.EmailField(null=True)
    numero_meses_vinculacion_Autor = models.DecimalField(null=True, max_digits=3, decimal_places=1)
    numero_Telefono_Autor = models.CharField(max_length=30, null=True)
    numero_horas_Semanales_dedicadas_Autores = models.IntegerField(null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    
class Participantes_Proyecto(models.Model):
    nombre_participantes_de_desarrollo = models.CharField(max_length=40, null=True)
    rol_Sennova_De_Participantes_de_Proyecto = models.CharField(max_length=50, choices=[('formulador', 'Formulador'), ('investigador', 'Investigador'), ('dinamizador', 'Dinamizador'), ('instructor', 'Instructor'), ('aprendiz','Aprendiz')], null=True)
    numero_cedula_participantes = models.BigIntegerField(null=True)
    numero_meses_vinculacion_participantes = models.DecimalField(null=True, max_digits=3, decimal_places=1)
    email_participantes_de_desarrollo = models.EmailField(null=True)
    numero_horas_Semanales_dedicadas_participantes = models.IntegerField(null=True)
    numero_Telefono_participantes = models.CharField(max_length=30, null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

# Preguntas politicas
class PreguntasP(models.Model):
    enunciado = models.CharField(max_length=200)
    estado = models.BooleanField()
    periodo = models.IntegerField()
    normalized = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        patterns_to_eliminate = [
            (" ", ""),
            ("¿", ""),
            ("?", ""),
            ("El", ""),
            ("el", ""),
            (".", ""),
        ]
        for patron, reemplazo in patterns_to_eliminate:
            self.normalized =unidecode(re.sub(re.escape(patron), reemplazo, self.normalized))
        super().save(*args, **kwargs)
         

class Generalidades_del_proyecto(models.Model):
    codigo_Dependencia_Presupuestal = models.CharField(max_length=50, null=True)
    tematicas_Estrategias_SENA = models.CharField(max_length=100, null=True)
    link_video_proyecto = models.CharField(max_length=500, null=True)
    actividades_economicas_del_proyecto_investigacion = models.CharField(max_length=100, null=True)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)

class Respuestas(models.Model):
    respuesta = models.CharField(max_length=600, null=False)
    pregunta = models.OneToOneField(PreguntasP, on_delete=models.CASCADE)
    generalidad = models.ForeignKey(Generalidades_del_proyecto, on_delete=models.CASCADE)

#Estructura del proyecto
class Resumen_antecedentes(models.Model):
    resumen_ejecutivo = models.TextField(max_length=8000, null=True)
    antecedentes = models.TextField(max_length=8000, null=True)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)


class Descripcion_problema(models.Model):
    identificacion_y_descripcion_problema = models.TextField(max_length=10000, null=False)
    justificacion = models.TextField(max_length=8000, null=True)
    marco_conceptual = models.TextField(max_length=11000, null=True)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)


# Objetivos
class Objetivos(models.Model):
    objetivo_general = models.CharField(max_length=500, null=True)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)

# Objetivos especificos
class Objetivos_especificos(models.Model):
    objetivo_especifico = models.CharField(max_length=500, null=True)
    actividades_obj_especificos = models.CharField(max_length=1000, null=True)
    causa = models.CharField(max_length=1000, null=True)
    efecto = models.CharField(max_length=1000, null=True)
    objetivoGeneral = models.ForeignKey(Objetivos, on_delete=models.CASCADE)


# Analisis de participantes
class Centro_de_formacion(models.Model):
    nombre_semillero_investigacion_beneficiados = models.CharField(null=True, max_length=300)
    numero_programas_beneficiarios_semilleros_investigacion = models.IntegerField(null=True)
    tipo_programas_formacion_beneficiados_conforman_semillero = models.CharField(null=True, max_length=300)
    nombre_programas_formacion_beneficiados_semillero = models.CharField(null=True, max_length=300)
    tipo_programas_de_formacion_beneficiados_por_ejecucion = models.CharField(null=True, max_length=300)
    nombre_programas_formacion_beneficiados_ejecucion_proyecto = models.CharField(null=True, max_length=300)
    numero_aprendices_participaran_ejecucion_proyecto = models.IntegerField(null=True)
    numero_municipios_beneficiados = models.IntegerField(null=True)
    nombre_municipios_beneficiados_descripcion_beneficio = models.CharField(null=True, max_length=300)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)

class Entidades_aliadas(models.Model):
    nombre_entidad = models.CharField(max_length=200, null=True)
    tipo_entidad_aliada = models.CharField(max_length=50, null=True)
    naturaleza_entidad = models.CharField(max_length=50, null=True)
    clasificacion_empresa = models.CharField(max_length=50, null=True)
    nit = models.CharField(max_length=30, null=True)
    convenio = models.BooleanField(null=True)
    especifique_tipo_codigo_convenio = models.CharField(max_length=50, null=True)
    recursos_especie_entidad = models.BigIntegerField(null=True)
    descripcion_recursos_especie_aportados = models.CharField(max_length=150, null=True)
    recursos_dinero_entidad_aliada = models.BigIntegerField(null=True)
    descripcion_destinacion_dinero_aportado = models.CharField(max_length=150, null=True)
    nombre_grupo_inv_entidad_aliada = models.CharField(max_length=170, null=True)
    codigo_gruplac_entidad_aliada = models.CharField(max_length=50, null=True)
    link_gruplac_entidad_aliada = models.CharField(max_length=500 ,null=True)
    actividades_desarrollar_entidad_aliada_marco_proyecto = models.CharField(max_length=1500, null=True)
    metodologia_act_transferencia_centro_formacion = models.CharField(max_length=500, null=True)
    objetivo_especificos = models.ManyToManyField(Objetivos_especificos)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

class Participantes_entidad_alidad(models.Model):
    nombre = models.CharField(max_length=150, null=True)
    numero_identificacion = models.BigIntegerField(null=True)
    email = models.EmailField(null=True)
    telefono = models.BigIntegerField(null=True)
    entidad = models.ForeignKey(Entidades_aliadas, on_delete=models.CASCADE)

# Resultados y productos esperados
class Resultados_y_productos_esperados(models.Model):
    tipo_resultado_esperado_obj_especifico = models.CharField(max_length=300, null=False)
    descripcion_resultado_esperado_obj_especifico = models.CharField(max_length=3000, null=False)
    nombre_producto_resultado_inv_obj_especifico = models.CharField(max_length=300, null=False)
    nombre_subtipologia = models.CharField(max_length=300, null=False)
    trl_producto_resultado_inv_obj_especifico = models.CharField(max_length=300, null=False)
    indicador_producto_resultado_inv_obj_especifico = models.CharField(max_length=300, null=False)
    fch_entrega_producto_resultado_inv_obj_especifico = models.DateField(null=False)
    objetivo_especifico = models.OneToOneField(Objetivos_especificos, on_delete=models.CASCADE)

# Proyeccion
class Proyeccion(models.Model):
    duracion = models.CharField(max_length=100,null=True)
    fch_inicio = models.DateField(null=True)
    fch_cierre = models.DateField(null=True)
    propuesta_sostenibilidad = models.CharField(max_length=500, null=True)
    impacto_social= models.CharField(max_length=500, null=True)
    impacto_tecnologico = models.CharField(max_length=500, null=True)
    impacto_centro_formacion = models.CharField(max_length=500, null=True)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)


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
    nombre = models.CharField(max_length=100, null=True)
    estado = models.BooleanField(default=True)
    vigencia = models.DateTimeField(auto_now=True)
    guia = models.FileField(upload_to='', null=True, blank=True)

class Anexos(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    anexo = models.FileField(upload_to='', null=True, blank=True)
    anexo_requerido = models.ForeignKey(Document, on_delete=models.CASCADE)
     
# Listas plegable
class Listas_plegables(models.Model):
    codigos_grupo_investigacion = models.CharField(max_length=10, null=True)
    nombre_grupo_investigacion = models.CharField(max_length=200, null=True)
    redes_conocimiento = models.CharField(max_length=200, null=True)
    subareas_conocimiento = models.CharField(max_length=200, null=True)
    diciplina_subarea = models.CharField(max_length=200, null=True)
    nombre_centro_formacion = models.CharField(max_length=200, null=True)
    actividades_economicas = models.CharField(max_length=250, null=True)

# Lista centros de formacion
class Region(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return str(self.nombre)
    
class Regional(models.Model):
    cod_regional = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=20)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cod_regional)
    
class Centro_formacion(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    cod_grupo_investigacion = models.CharField(max_length=10, null=True)
    region = models.ForeignKey(Regional, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.codigo)
    
#Middleware
class UltimaVista(models.Model):
    usuario = models.OneToOneField(Usuarios, on_delete=models.CASCADE)
    ultima_vista = models.CharField(max_length=255, null=True)
    
#Rubros
class TipoRubro(models.Model):
    # codigo = models.CharField(primary_key=True) Voy a trabajar con el ID para mas facilidad al obtenerlo, si papi Gus nos da un codigo alfanumerico lo cambiamos.
    descripcion = models.CharField(max_length=500)

class Rubro(models.Model):
    # codigo = models.CharField(primary_key=True) Lo mismo con esto.
    tipo = models.ForeignKey(TipoRubro, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=500)
    estado = models.BooleanField()


#Recursos
class CronogramaAct(models.Model):
    fch_inicio = models.DateField(null=True)
    fch_cierre = models.DateField(null=True)
    observacion = models.CharField(max_length=800, null=True)
    actividad = models.OneToOneField(Objetivos_especificos, on_delete=models.CASCADE)
    actorEntidad = models.ManyToManyField(Entidades_aliadas)
    actorParticipante = models.ManyToManyField(Participantes_entidad_alidad)

class Presupuesto(models.Model):
    valor = models.BigIntegerField()
    actividad = models.OneToOneField(Objetivos_especificos, on_delete=models.CASCADE)
    tipoRubro = models.OneToOneField(TipoRubro, on_delete=models.CASCADE)
    rubro = models.OneToOneField(Rubro, on_delete=models.CASCADE)
