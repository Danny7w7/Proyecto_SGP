
document.addEventListener("DOMContentLoaded", function() {
    
    const allValidations = {
        //Estructura del proyecto
       "form1": {
        "resumen_ejecutivo": {
            pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{5,7000}$/u,
            errorMsg: 'El resumen ejecutivo no es válido. Debe tener entre 5 y 7000 caracteres.'
        },
        "antecedentes": {
            pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{5,7000}$/u,
            errorMsg: 'El antecedente no es válido. Debe tener entre 5 y 7000 caracteres.'
        },
       },

    //Descripcion del problema
       "form2":{
        "identificacion_y_descripcion_problema": {
            pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{5,7000}$/u,
            errorMsg: 'La identificación y descripcion del problema no es válido. Debe tener entre 5 y 7000 caracteres.'
        },
        "justificacion": {
            pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{5,7000}$/u,
            errorMsg: 'La justificación no es válida. Debe tener entre 5 y 7000 caracteres.'
        },
        "marco_conceptual": {
            pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{5,7000}$/u,
            errorMsg: 'El marco conceptual no es válido. Debe tener entre 5 y 7000 caracteres.'
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
        handleFormSubmit(event, 'form1');
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

function sendPost1() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    // Obtener los valores de los campos del formulario
    var resumen_ejecutivo = document.getElementById("resumen_ejecutivo").value;
    var antecedentes = document.getElementById("antecedentes").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("Resumen_ejecutivo", resumen_ejecutivo);
    formData.append("Antecedentes", antecedentes);
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/est-proyecto/resumen-antecedentes/${id_proyecto}/`, {
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
    var identificacion_y_descripcion_problema = document.getElementById("identificacion_y_descripcion_problema").value;
    var justificacion = document.getElementById("justificacion").value;
    var marco_conceptual = document.getElementById("marco_conceptual").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("Identificacion_y_descripcion_problema", identificacion_y_descripcion_problema);
    formData.append("Justificacion", justificacion);
    formData.append("Marco_conceptual", marco_conceptual);
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/est-proyecto/descripcion-problema/${id_proyecto}/`, {
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
            window.location.href = `/objetivos/${id_proyecto}/`;
        }
    })
    .catch(error => {
        console.error('Error en la solicitud:', error);
        // Manejar errores en la solicitud, como problemas de red
    });
};

