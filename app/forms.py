# forms.py
from django import forms
from .models import Proyecto, Informacion_de_centro, Autores, Participantes_Proyecto, Informacion_Proyecto

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