# forms.py
from django import forms
from .models import Proyecto, Informacion_de_centro, Autores, Participantes_Proyecto, Informacion_Proyecto, Estructura_del_proyecto, Analisis_Participantes, Entidades_aliadas, RiesgoObjetivoGeneral, RiesgoProductos, RiesgoActividades, Estructura_arbol_problemas, Estructura_problema 

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'

# Informacion proponente
class Informacion_de_centroForm(forms.ModelForm):
    class Meta:
        model = Informacion_de_centro
        fields = '__all__'

class AutoresForm(forms.ModelForm):
    class Meta:
        model = Autores
        fields = '__all__'

class ParticipantesForm(forms.ModelForm):
    class Meta:
        model = Participantes_Proyecto
        fields = '__all__'

#Generalidades
class Informacion_ProyectoForm(forms.ModelForm):
    class Meta:
        model = Informacion_Proyecto
        fields = '__all__'

class Estructura_del_proyectoForm(forms.ModelForm):
    class Meta:
        model = Estructura_del_proyecto
        fields = '__all__'

class Estructura_arbol_problemasForm(forms.ModelForm):
    class Meta:
        model = Estructura_arbol_problemas
        fields = '__all__'

class Estructura_problemaForm(forms.ModelForm):
    class Meta:
        model = Estructura_problema
        fields = '__all__'

class Analisis_ParticipantesForm(forms.ModelForm):
    class Meta:
        model = Analisis_Participantes
        fields = '__all__'

class Entidades_aliadasForm(forms.ModelForm):
    class Meta:
        model = Entidades_aliadas
        fields = '__all__'

class RiesgoObjetivoGeneralForm(forms.ModelForm):
    class Meta:
        model = RiesgoObjetivoGeneral
        fields = '__all__'

class RiesgoProductosForm(forms.ModelForm):
    class Meta:
        model = RiesgoProductos
        fields = '__all__'

class RiesgoActividadesForm(forms.ModelForm):
    class Meta:
        model = RiesgoActividades
        fields = '__all__'

