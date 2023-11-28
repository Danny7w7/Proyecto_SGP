from django.contrib import admin

from .models import Usuarios, Roles, Objetivos
admin.site.register(Usuarios)
admin.site.register(Roles)
admin.site.register(Objetivos)