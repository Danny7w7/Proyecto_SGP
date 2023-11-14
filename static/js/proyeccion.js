document.getElementById("fecha_inicio").addEventListener("change", comprobarFechas);
document.getElementById("fecha_cierre").addEventListener("change", comprobarFechas);

function comprobarFechas() {
    var inputDuracion = document.getElementById("duracion_proyecto")
    var fechaInicio = new Date(document.getElementById("fecha_inicio").value);
    var fechaCierre = new Date(document.getElementById("fecha_cierre").value);

    if (!isNaN(fechaInicio) && !isNaN(fechaCierre) && fechaInicio < fechaCierre) {
        const duracion = calcularDuracionEnSemanasYDias(fechaInicio, fechaCierre);
        inputDuracion.value = `La duración es de ${duracion.semanas} semanas y ${duracion.diasRestantes} días`
    } else {
        inputDuracion.value = "Por favor, completa ambas fechas."
    }
}

document.addEventListener("DOMContentLoaded", function() {
    
    const allValidations = {
        //Estructura del proyecto
       "form1": {
        "duracion_proyecto": {
            pattern: /^[\w\s.,?!;:'"()\-–—Ññ]{5,250}$/,
            errorMsg: 'El resumen no es válido. Debe tener entre 5 y 250 caracteres.'
        },
        "fecha_inicio": {
            pattern: /^[\w\s.,?!;:'"()\-–—Ññ]{5,250}$/,
            errorMsg: 'El resumen no es válido. Debe tener entre 5 y 250 caracteres.'
        },
        "fecha_cierre": {
            pattern: /^[\w\s.,?!;:'"()\-–—Ññ]{5,250}$/,
            errorMsg: 'El resumen no es válido. Debe tener entre 5 y 250 caracteres.'
        }
       },

    //Descripcion del problema
       "form2":{
        "propuesta_sostenibilidad": {
            pattern: /^[\w\s.,?!;:'"()\-–—Ññ]{5,250}$/,
            errorMsg: 'Identificación y descripción no es válido. Debe tener entre 5 y 250 caracteres.'
        },
        "impacto_social": {
            pattern: /^[\w\s.,?!;:'"()\-–—Ññ]{5,250}$/,
            errorMsg: 'Identificación y descripción no es válido. Debe tener entre 5 y 250 caracteres.'
        },
        "impacto_tecnologico": {
            pattern: /^[\w\s.,?!;:'"()\-–—Ññ]{5,250}$/,
            errorMsg: 'Identificación y descripción no es válido. Debe tener entre 5 y 250 caracteres.'
        },
        "impacto_centro": {
            pattern: /^[\w\s.,?!;:'"()\-–—Ññ]{5,250}$/,
            errorMsg: 'Identificación y descripción no es válido. Debe tener entre 5 y 250 caracteres.'
        },
       },
    };

    // Itera sobre cada conjunto de validaciones
    for (let formKey in allValidations) {
        for (let fieldId in allValidations[formKey]) {
            const inputField = document.getElementById(fieldId);
            
            // Verifica si el inputField realmente existe
            if(!inputField) {
                console.error(`El campo con id ${fieldId} no fue encontrado.`);
                continue;
            }

            const feedbackElement = inputField.nextElementSibling;
            const { pattern, errorMsg } = allValidations[formKey][fieldId];

            inputField.addEventListener("input", function() {
                validateField(inputField, feedbackElement, pattern, errorMsg);
            });
        }
    }

//ids de los formularios
    const form1 = document.getElementById("form1");
    const form2 = document.getElementById("form2");


    document.getElementById("enviar1").addEventListener("click", function() {
        sendPost1()
    });
    document.getElementById("enviar2").addEventListener("click", function() {
        handleFormSubmit(event, 'form2');
    });

    function handleFormSubmit(event, formKey) {
        let isValid = true;
        
        for (let fieldId in allValidations[formKey]) {
            const inputField = document.getElementById(fieldId);
                
            // Nueva comprobación para evitar errores
            if(!inputField) continue;

            const feedbackElement = inputField.nextElementSibling;
            const { pattern, errorMsg } = allValidations[formKey][fieldId];

            isValid = validateField(inputField, feedbackElement, pattern, errorMsg) && isValid;
        }
        event.preventDefault();
        if (isValid) {
            Swal.fire({
                title: '¡Éxito!',
                text: 'Información registrada correctamente.',
                icon: 'success',
                confirmButtonText: 'Aceptar'
            }).then(() => {
                if (formKey == 'form1'){
                    sendPost1()
                }else if (formKey == 'form2'){
                    sendPost2()
                }
            });
        }else{
            Swal.fire({
                title: 'Error!',
                text: 'Por favor, corrija los errores en el formulario antes de enviar.',
                icon: 'error',
                confirmButtonText: 'Aceptar'
            });
        }
    }

    function validateField(field, feedback, pattern, errorMsg) {
        if (pattern.test(field.value)) {
            field.classList.remove("is-invalid");
            field.classList.add("is-valid");
            feedback.textContent = '';
            return true;
        } else {
            field.classList.remove("is-valid");
            field.classList.add("is-invalid");
            feedback.textContent = errorMsg;
            return false;
        }
    }
});


function calcularDuracionEnSemanasYDias(fechaInicio, fechaFin) {
    // Calcula la diferencia en milisegundos entre las dos fechas
    const diferenciaEnMilisegundos = fechaFin - fechaInicio;
  
    // Convierte la diferencia en días
    const diferenciaEnDias = diferenciaEnMilisegundos / (1000 * 60 * 60 * 24);
  
    // Calcula el número de semanas
    const semanas = Math.floor(diferenciaEnDias / 7);
  
    // Calcula el número de días restantes
    const diasRestantes = diferenciaEnDias % 7;
  
    return { semanas, diasRestantes };
}

function sendPost1() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    // Obtener los valores de los campos del formulario
    
    var duracion_proyecto = document.getElementById("duracion_proyecto").value;
    var fecha_inicio = document.getElementById("fecha_inicio").value;
    var fecha_cierre = document.getElementById("fecha_cierre").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("duracion", duracion_proyecto);
    formData.append("fch_inicio", fecha_inicio);
    formData.append("fch_cierre", fecha_cierre);
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/proyeccion/tiempo-ejecucion/${id_proyecto}/`, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())  // Parsea la respuesta JSON
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
            // Manejar el error, por ejemplo, mostrar un mensaje de error al usuario
        } else {
            console.log('Mensaje de éxito:', data.mensaje);
            // Realizar acciones de éxito, si es necesario
        }
    })
    .catch(error => {
        console.error('Error en la solicitud:', error);
        // Manejar errores en la solicitud, como problemas de red
    });
};

function sendPost2() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    // Obtener los valores de los campos del formulario
    var formFile = document.getElementById("formFile").files[0];
    var propuesta_sostenibilidad = document.getElementById("propuesta_sostenibilidad").value;
    var impacto_social = document.getElementById("impacto_social").value;
    var impacto_tecnologico = document.getElementById("impacto_tecnologico").value;
    var impacto_centro = document.getElementById("impacto_centro").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("Cadena_valor", formFile);
    formData.append("Propuesta_sostenibilidad", propuesta_sostenibilidad);
    formData.append("Impacto_social", impacto_social);
    formData.append("Impacto_tecnologico", impacto_tecnologico);
    formData.append("Impacto_centro", impacto_centro);
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/proyeccion/cadena-de-valor/${id_proyecto}/`, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())  // Parsea la respuesta JSON
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
            // Manejar el error, por ejemplo, mostrar un mensaje de error al usuario
        } else {
            console.log('Mensaje de éxito:', data.mensaje);
            window.location.href = `/analisis-riesgo/${id_proyecto}/`;
        }
    })
    .catch(error => {
        console.error('Error en la solicitud:', error);
        // Manejar errores en la solicitud, como problemas de red
    });
};

