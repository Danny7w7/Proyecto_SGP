from django.shortcuts import render

def mostrar_error(request, mensaje):
    context = {
        'percentaje': 0 ,
        'mensaje_error': mensaje}
    return render(request, 'error.html', context)