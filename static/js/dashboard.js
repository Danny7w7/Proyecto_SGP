document.addEventListener('DOMContentLoaded', function() {
    $.ajax({
        url: '/dashboard/lista-codigos/',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            console.log(response);
            if (response.data && response.data.length > 0) {
                var itemsPorPagina = 10;
                var datosFiltrados = filtrarDatos(response.data);
                iniciarTabla(datosFiltrados, itemsPorPagina);
            } else {
                console.error('Error en la respuesta del servidor');
            }
        },
        error: function(error) {
            console.error('Error en la solicitud AJAX', error);
        }
    });

    function filtrarDatos(datos) {
        return datos.filter(function(item) {
            return item.nombre_grupo_investigacion && item.codigos_grupo_investigacion;
        });
    }

    function iniciarTabla(data, itemsPorPagina) {
        var tabla = $('#tablaDatos tbody');
        var paginacion = $('#paginacion');
        var paginaActual = 1;

        function mostrarPagina(pagina) {
            var inicio = (pagina - 1) * itemsPorPagina;
            var fin = inicio + itemsPorPagina;

            tabla.empty();

            for (var i = inicio; i < fin && i < data.length; i++) {
                var fila = '<tr><td>' + data[i].nombre_grupo_investigacion + '</td><td>' + data[i].codigos_grupo_investigacion + '</td></tr>';
                tabla.append(fila);
            }
        }

        function crearBoton(pagina) {
            var boton = $('<button>').text(pagina).click(function() {
                mostrarPagina(pagina);
            });

            // Aplicar estilos directamente a los botones
            boton.css({
                'margin-right': '5px',
                'padding': '5px 10px',
                'background-color': '#4e73df',
                'color': '#fff',
                'border': 'none',
                'border-radius': '3px',
                'cursor': 'pointer'
            });

            boton.hover(function() {
                $(this).css('background-color', '#4e73df');
            }, function() {
                $(this).css('background-color', '#224abe');
            });

            return boton;
        }

        function actualizarPaginacion() {
            paginacion.empty();
            for (var i = 1; i <= Math.ceil(data.length / itemsPorPagina); i++) {
                paginacion.append(crearBoton(i));
            }
        }

        mostrarPagina(paginaActual);
        actualizarPaginacion();
    }
});
//  Fin tabla 1

//Inico tabla 2
document.addEventListener('DOMContentLoaded', function() {
    $.ajax({
        url: '/dashboard/lista-codigos2/',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            console.log(response);
            if (response.data && response.data.length > 0) {
                var itemsPorPagina = 10;
                var datosFiltrados = filtrarDatos(response.data);
                iniciarTabla(datosFiltrados, itemsPorPagina);
            } else {
                console.error('Error en la respuesta del servidor');
            }
        },
        error: function(error) {
            console.error('Error en la solicitud AJAX', error);
        }
    });

    function filtrarDatos(datos) {
        return datos.filter(function(item) {
            return item.redes_conocimiento;
        });
    }

    function iniciarTabla(data, itemsPorPagina) {
        var tabla = $('#tablaDatos2 tbody');
        var paginacion = $('#paginacion2');
        var paginaActual = 1;

        function mostrarPagina(pagina) {
            var inicio = (pagina - 1) * itemsPorPagina;
            var fin = inicio + itemsPorPagina;

            tabla.empty();

            for (var i = inicio; i < fin && i < data.length; i++) {
                var fila = '<tr><td>' + data[i].redes_conocimiento + '</td>';
                tabla.append(fila);
            }
        }

        function crearBoton(pagina) {
            var boton = $('<button>').text(pagina).click(function() {
                mostrarPagina(pagina);
            });

            // Aplicar estilos directamente a los botones
            boton.css({
                'margin-right': '5px',
                'padding': '5px 10px',
                'background-color': '#4e73df',
                'color': '#fff',
                'border': 'none',
                'border-radius': '3px',
                'cursor': 'pointer'
            });

            boton.hover(function() {
                $(this).css('background-color', '#4e73df');
            }, function() {
                $(this).css('background-color', '#224abe');
            });

            return boton;
        }

        function actualizarPaginacion() {
            paginacion.empty();
            for (var i = 1; i <= Math.ceil(data.length / itemsPorPagina); i++) {
                paginacion.append(crearBoton(i));
            }
        }

        mostrarPagina(paginaActual);
        actualizarPaginacion();
    }
});
//Fin tabla 2

//Inico tabla 3
document.addEventListener('DOMContentLoaded', function() {
    $.ajax({
        url: '/dashboard/lista-codigos3/',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            console.log(response);
            if (response.data && response.data.length > 0) {
                var itemsPorPagina = 10;
                var datosFiltrados = filtrarDatos(response.data);
                iniciarTabla(datosFiltrados, itemsPorPagina);
            } else {
                console.error('Error en la respuesta del servidor');
            }
        },
        error: function(error) {
            console.error('Error en la solicitud AJAX', error);
        }
    });

    function filtrarDatos(datos) {
        return datos.filter(function(item) {
            return item.subareas_conocimiento;
        });
    }

    function iniciarTabla(data, itemsPorPagina) {
        var tabla = $('#tablaDatos3 tbody');
        var paginacion = $('#paginacion3');
        var paginaActual = 1;

        function mostrarPagina(pagina) {
            var inicio = (pagina - 1) * itemsPorPagina;
            var fin = inicio + itemsPorPagina;

            tabla.empty();

            for (var i = inicio; i < fin && i < data.length; i++) {
                var fila = '<tr><td>' + data[i].subareas_conocimiento + '</td>';
                tabla.append(fila);
            }
        }

        function crearBoton(pagina) {
            var boton = $('<button>').text(pagina).click(function() {
                mostrarPagina(pagina);
            });

            // Aplicar estilos directamente a los botones
            boton.css({
                'margin-right': '5px',
                'padding': '5px 10px',
                'background-color': '#4e73df',
                'color': '#fff',
                'border': 'none',
                'border-radius': '3px',
                'cursor': 'pointer'
            });

            boton.hover(function() {
                $(this).css('background-color', '#4e73df');
            }, function() {
                $(this).css('background-color', '#224abe');
            });

            return boton;
        }

        function actualizarPaginacion() {
            paginacion.empty();
            for (var i = 1; i <= Math.ceil(data.length / itemsPorPagina); i++) {
                paginacion.append(crearBoton(i));
            }
        }

        mostrarPagina(paginaActual);
        actualizarPaginacion();
    }
});
//Fin tabla 3

//Inico tabla 4
document.addEventListener('DOMContentLoaded', function() {
    $.ajax({
        url: '/dashboard/lista-codigos4/',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            console.log(response);
            if (response.data && response.data.length > 0) {
                var itemsPorPagina = 10;
                var datosFiltrados = filtrarDatos(response.data);
                iniciarTabla(datosFiltrados, itemsPorPagina);
            } else {
                console.error('Error en la respuesta del servidor');
            }
        },
        error: function(error) {
            console.error('Error en la solicitud AJAX', error);
        }
    });

    function filtrarDatos(datos) {
        return datos.filter(function(item) {
            return item.diciplina_subarea;
        });
    }

    function iniciarTabla(data, itemsPorPagina) {
        var tabla = $('#tablaDatos4 tbody');
        var paginacion = $('#paginacion4');
        var paginaActual = 1;

        function mostrarPagina(pagina) {
            var inicio = (pagina - 1) * itemsPorPagina;
            var fin = inicio + itemsPorPagina;

            tabla.empty();

            for (var i = inicio; i < fin && i < data.length; i++) {
                var fila = '<tr><td>' + data[i].diciplina_subarea + '</td>';
                tabla.append(fila);
            }
        }

        function crearBoton(pagina) {
            var boton = $('<button>').text(pagina).click(function() {
                mostrarPagina(pagina);
            });

            boton.css({
                'margin-right': '5px',
                'padding': '5px 10px',
                'background-color': '#4e73df',
                'color': '#fff',
                'border': 'none',
                'border-radius': '3px',
                'cursor': 'pointer'
            });

            boton.hover(function() {
                $(this).css('background-color', '#4e73df');
            }, function() {
                $(this).css('background-color', '#224abe');
            });

            return boton;
        }

        function actualizarPaginacion() {
            paginacion.empty();
            for (var i = 1; i <= Math.ceil(data.length / itemsPorPagina); i++) {
                paginacion.append(crearBoton(i));
            }
        }

        mostrarPagina(paginaActual);
        actualizarPaginacion();
    }
});
// Fin tabla 4

//Inicio tabla 5
document.addEventListener('DOMContentLoaded', function() {
    $.ajax({
        url: '/dashboard/lista-codigos5/',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            console.log(response);
            if (response.data && response.data.length > 0) {
                var itemsPorPagina = 10;
                var datosFiltrados = filtrarDatos(response.data);
                iniciarTabla(datosFiltrados, itemsPorPagina);
            } else {
                console.error('Error en la respuesta del servidor');
            }
        },
        error: function(error) {
            console.error('Error en la solicitud AJAX', error);
        }
    });

    function filtrarDatos(datos) {
        return datos.filter(function(item) {
            return item.nombre_centro_formacion;
        });
    }

    function iniciarTabla(data, itemsPorPagina) {
        var tabla = $('#tablaDatos5 tbody');
        var paginacion = $('#paginacion5');
        var paginaActual = 1;

        function mostrarPagina(pagina) {
            var inicio = (pagina - 1) * itemsPorPagina;
            var fin = inicio + itemsPorPagina;

            tabla.empty();

            for (var i = inicio; i < fin && i < data.length; i++) {
                var fila = '<tr><td>' + data[i].nombre_centro_formacion + '</td>';
                tabla.append(fila);
            }
        }

        function crearBoton(pagina) {
            var boton = $('<button>').text(pagina).click(function() {
                mostrarPagina(pagina);
            });

            boton.css({
                'margin-right': '5px',
                'padding': '5px 10px',
                'background-color': '#4e73df',
                'color': '#fff',
                'border': 'none',
                'border-radius': '3px',
                'cursor': 'pointer'
            });

            boton.hover(function() {
                $(this).css('background-color', '#4e73df');
            }, function() {
                $(this).css('background-color', '#224abe');
            });

            return boton;
        }

        function actualizarPaginacion() {
            paginacion.empty();
            for (var i = 1; i <= Math.ceil(data.length / itemsPorPagina); i++) {
                paginacion.append(crearBoton(i));
            }
        }

        mostrarPagina(paginaActual);
        actualizarPaginacion();
    }
});

