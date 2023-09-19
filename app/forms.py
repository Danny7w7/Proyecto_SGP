# forms.py
from django import forms
from .models import Proyecto
from .models import Informacion_de_centro
from .models import Autores

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