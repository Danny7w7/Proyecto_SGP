
from django.utils.deprecation import MiddlewareMixin
from .models import UltimaVista

class ActualizarUltimaVistaMiddleware(MiddlewareMixin):
    EXCLUIDAS = [

    #Administrador y privadas
    '/continuar-sesion/', '/register/', '/logout/', '/recuperar-contrasena/',
    #Proyecto
    '/proyectos_usuario/' , '/edit_proyec/<int:id_proyecto>/','/editar_objetivo/<int:id_proyecto>/',
    '/editar_anexo/<int:proyecto_id>/',
    '/eliminar_usuario/<int:usuario_id>/',

    #Formulador
    '/Dashboard/', '/Dashboard/Doc-Anexos/', '/Dashboard/Usuarios/', '/Dashboard/PreguntasPoli',
    '/Dashboard/Proyectos-Inactivos/','/Dashboard/Proyectos-Completos/','/Dashboard/Proyectos-Inactivos/',
    '/Dashboard/Proyectos-Pendientes/','/Dashboard/404/notfount/' 

    #Anexo
    '/editar_anexo/<int:proyecto_id>/',
    # PDF
        '/generar_pdf/<int:proyecto_id>/',
        '/generar_c_valor/<int:proyecto_id>/',
    ]

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            if request.path not in self.EXCLUIDAS:
                UltimaVista.objects.update_or_create(
                    usuario=request.user,
                    defaults={'ultima_vista': request.path}
                )
        return None