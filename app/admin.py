from django.contrib import admin

from .models import Usuarios, Roles, Objetivos, Region, Regional, Centro_formacion
admin.site.register(Usuarios)
admin.site.register(Roles)
admin.site.register(Objetivos)
admin.site.register(Region)
admin.site.register(Regional)
admin.site.register(Centro_formacion)