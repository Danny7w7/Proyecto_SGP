document.addEventListener("DOMContentLoaded", function() {
    const allValidations = {
       "form1": {
        "nombre": {
            pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,50}$/u,
            errorMsg: 'El nombre no es válido. Debe tener entre 5 y 50 caracteres y solo puede contener letras y espacios'
        },
        "numero_identificacion": {
            pattern: /^\d{6,20}$/,
            errorMsg: 'El número no es válido. Debe tener 6 digitos númericos',
        },
        "email": {
            pattern: /^[a-zA-Z0-9._%+-ñÑ,]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
            errorMsg: 'El correo no es válido. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        },
        "telefono": {
            pattern: /^\d{10}$/,
            errorMsg: 'El número no es válido. Debe tener 10 digitos númericos',
        },
       }
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


    document.getElementById("enviar1").addEventListener("click", function(event) {
        handleFormSubmit(event, 'form1');
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
                sendPost1()
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
        }else{
            field.classList.remove("is-valid");
            field.classList.add("is-invalid");
            feedback.textContent = errorMsg;
            return false;
        }
    }
});

function sendPost1() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    var id_entidad = document.getElementById("id_entidad").value;
    // Obtener los valores de los campos del formulario
    var nombre = document.getElementById("nombre").value; 
    var numero_identificacion = document.getElementById("numero_identificacion").value;
    var email = document.getElementById("email").value;
    var telefono = document.getElementById("telefono").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("nombre", nombre);
    formData.append("numero_identificacion", numero_identificacion);
    formData.append("email", email);
    formData.append("telefono", telefono);
    formData.append("id_entidad", id_entidad);
    console.log(id_entidad)
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/participantes-entidad/${id_proyecto}/`, {
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
            
            let tableBody = document.querySelector('.table tbody');
            let newRow = tableBody.insertRow();
            
            newRow.insertCell(0).textContent = data.nuevo_participante.nombre;
            newRow.insertCell(1).textContent = data.nuevo_participante.numero_identificacion;
            newRow.insertCell(2).textContent = data.nuevo_participante.email;
            newRow.insertCell(3).textContent = data.nuevo_participante.telefono;
        }
    })
    .catch(error => {
        console.error('Error en la solicitud:', error);
        // Manejar errores en la solicitud, como problemas de red
    });
};