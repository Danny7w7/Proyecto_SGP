

try {
    document.getElementById('clickPassword').addEventListener('click', () => {
        $('#myModal').modal({
            keyboard: false
          })
        contrasena = document.getElementById('clickPassword').textContent
        navigator.clipboard.writeText(contrasena)
    })
  } catch (error) {
    console.error("Ocurrió un error:", error);
  }
  
// Funcion mostrar usuarios
document.addEventListener('DOMContentLoaded', function () {
    var usuariosContainer = document.getElementById('usuarios-container');
    try {
        if (!usuariosContainer) {
            throw new Error('El elemento #usuarios-container no fue encontrado en el DOM.');
        }
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var data = JSON.parse(xhr.responseText);
                    usuariosContainer.textContent = data.cantidad_usuarios;
                } else {
                    console.error('Error en la solicitud: ', xhr.status);
                }
            }
        };
        xhr.open('GET', '/dashboard/count-usuarios/', true);
        xhr.send();
    } catch (error) {
        console.error('Error: ', error.message);
    }
});

// Codigo para eliminar usuarios.
$(document).ready(function () {
    $('.eliminar-usuario').on('click', function () {
        var usuarioId = $(this).data('usuario-id');
        if (confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
            var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            $.ajax({
                url: '/eliminar_usuario/' + usuarioId + '/',
                type: 'POST',
                dataType: 'json',
                success: function (data) {
                    alert(data.mensaje);
                },
                error: function () {
                    alert('Error al eliminar el usuario.');
                }
            });
        }
    });
});


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
//Fin tabla 5


// Funcionalidades de guardado
// modal1
$(document).ready(function () {
    function abrirModal() {
      $("#myModal").modal("show");
    }

    $(".tabla1").click(abrirModal);

    // Solicitud AJAX
    $("#mi-formulario").submit(function (e) {
      e.preventDefault();

      var formData = $(this).serialize();

      $.ajax({
        type: "POST",
        url: "/dashboard/agregar-grupo-code/",
        data: formData,
        success: function (response) {
          if (response.status === "success") {
            alert("Datos agregados exitosamente");
            // Puedes recargar la tabla u otras actualizaciones aquí
          } else {
            alert("Error al agregar datos");
          }
        },
        error: function () {
          alert("Error de conexión");
        },
        complete: function () {
          $("#myModal").modal("hide");
        },
      });
    });
  });

// modal2
  $(document).ready(function () {
    function abrirModal() {
      $("#myModal2").modal("show");
    }

    $(".tabla2").click(abrirModal);

    // Solicitud AJAX
    $("#mi-formulario2").submit(function (e) {
      e.preventDefault();

      var formData = $(this).serialize();

      $.ajax({
        type: "POST",
        url: "/dashboard/redes-conocimiento/",
        data: formData,
        success: function (response) {
          if (response.status === "success") {
            alert("Datos agregados exitosamente");
          } else {
            alert("Error al agregar datos");
          }
        },
        error: function () {
          alert("Error de conexión");
        },
        complete: function () {
          $("#myModal2").modal("hide");
        },
      });
    });
  });

// modal3
$(document).ready(function () {
    function abrirModal() {
      $("#myModal3").modal("show");
    }

    $(".tabla3").click(abrirModal);

    // Solicitud AJAX
    $("#mi-formulario3").submit(function (e) {
      e.preventDefault();

      var formData = $(this).serialize();

      $.ajax({
        type: "POST",
        url: "/dashboard/subareas-conocimiento/",
        data: formData,
        success: function (response) {
          if (response.status === "success") {
            alert("Datos agregados exitosamente");
          } else {
            alert("Error al agregar datos");
          }
        },
        error: function () {
          alert("Error de conexión");
        },
        complete: function () {
          $("#myModal3").modal("hide");
        },
      });
    });
  });

// modal4
$(document).ready(function () {
    function abrirModal() {
      $("#myModal4").modal("show");
    }

    $(".tabla4").click(abrirModal);

    // Solicitud AJAX
    $("#mi-formulario4").submit(function (e) {
      e.preventDefault();

      var formData = $(this).serialize();

      $.ajax({
        type: "POST",
        url: "/dashboard/disciplina-subarea/",
        data: formData,
        success: function (response) {
          if (response.status === "success") {
            alert("Datos agregados exitosamente");
          } else {
            alert("Error al agregar datos");
          }
        },
        error: function () {
          alert("Error de conexión");
        },
        complete: function () {
          $("#myModal4").modal("hide");
        },
      });
    });
  });

// Agregar preguntas politicas
function addPreguntas(){
    var formData = new FormData();
    formData.append("iPregunta", document.getElementById('iPregunta').value);
    formData.append("iPeriodo", document.getElementById('iPeriodo').value);
    formData.append("csrfmiddlewaretoken", document.querySelector('[name=csrfmiddlewaretoken]').value);
    
    fetch(`/dashboard/addquestion/`, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())  // Parsea la respuesta JSON
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
        } else {
            console.log('Mensaje de éxito:', data.mensaje);
            $('#addPreguntaPolitica').modal('hide')
            $('#successModal').modal('show')
            updateTablePregunta(data)
        }
    })
    // .catch(error => {
    //     console.error('Error en la solicitud:', error);
    //     // Manejar errores en la solicitud, como problemas de red
    // });
}

function updateTablePregunta(data){
    let table = document.getElementById('tablequestion')
    let nuevaFila = table.insertRow();
    nuevaFila.insertCell().textContent = data.question.enunciado;
    nuevaFila.insertCell().textContent = data.question.periodo;
    nuevaFila.insertCell().textContent = data.question.estado;
}

// Funcion de agregar nuevo anexo
function agregarAnexo() {
    var nombre_anexo = prompt("Ingrese el nombre del nuevo anexo:");

    if (nombre_anexo !== null) {
        var estado_anexo = confirm("¿Desea mostrar este anexo?");
        estado_anexo = estado_anexo === true || estado_anexo === "true";

        $.ajax({
            type: 'POST',
            url: '/guardar_anexo/',
            data: {
                'nombre_anexo': nombre_anexo,
                'estado_anexo': estado_anexo.toString()
            },
            success: function (response) {
                if (response.success) {
                    alert('Anexo agregado exitosamente');

                    // Actualizar la tabla con los nuevos datos
                    actualizarTabla(response.nuevos_anexos);
                } else {
                    alert('Error al agregar el anexo');
                }
            },
            error: function (error) {
                console.error('Error en la solicitud AJAX: ' + error.responseText);
            }
        });
    }
}


function cargarGuia(documentId) {
    // Crear un input de tipo archivo
    var inputFile = document.createElement('input');
    inputFile.type = 'file';
    inputFile.accept = '.pdf','.docx'; // O el tipo de archivo que desees permitir
    inputFile.style.display = 'none'; // Ocultar el input

    // Función para manejar el cambio de archivo seleccionado
    inputFile.onchange = function(event) {
        var formData = new FormData();
        var archivo = event.target.files[0];
        formData.append('guia', archivo);
        formData.append('document_id', documentId);

        // Enviar el archivo al servidor
        $.ajax({
            type: 'POST',
            url: '/cargar_guia/',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    alert('Documento guía cargado correctamente');
                    // Puedes realizar alguna acción adicional aquí si es necesario, como actualizar la página
                } else {
                    alert('Error al cargar el documento guía: ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error al cargar el documento guía:', error);
                alert('Error al cargar el documento guía');
            }
        });
    };

    // Simular clic en el input de tipo archivo
    inputFile.click();
}putFile.click();
