
from django.utils.deprecation import MiddlewareMixin
from .models import UltimaVista

class ActualizarUltimaVistaMiddleware(MiddlewareMixin):
    EXCLUIDAS = ['/continuar-sesion/', '/register/', '/logout/', '/recuperar-contrasena/', '/proyectos_usuario/' , 
                 '/edit_proyec/<int:id_proyecto>/','/editar_objetivo/<int:id_proyecto>/','/Dashboard/', '/Dashboard/Doc-Anexos/', 
                 '/Dashboard/Usuarios/', '/Dashboard/PreguntasPoli',
                 '/Dashboard/Proyectos-Inactivos/','/Dashboard/Proyectos-Completos/','/Dashboard/Proyectos-Inactivos/',
                 '/Dashboard/Proyectos-Pendientes/','/Dashboard/404/notfount/']

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            if request.path not in self.EXCLUIDAS:
                UltimaVista.objects.update_or_create(
                    usuario=request.user,
                    defaults={'ultima_vista': request.path}
                )
        return None