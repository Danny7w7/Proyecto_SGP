
document.addEventListener("DOMContentLoaded", function() {
    
    const allValidations = {
        //Riesgos nivel objetivo general
       "form1": {
        "descripcion": {
            pattern: /^[\w\s.,?!;:'"()\-–—]{5,150}$/,
            errorMsg: 'La descripción no es válida. Debe tener entre 5 y 150 caracteres.'
        },
        "efectos": {
            pattern: /^[\w\s.,?!;:'"()\-–—]{5,150}$/,
            errorMsg: 'Los efectos no son válidos. Debe tener entre 5 y 150 caracteres.'
        },
        "medidas_Mitigacion": {
            pattern: /^[\w\s.,?!;:'"()\-–—]{5,150}$/,
            errorMsg: 'Las medidas de mitigación no son válidas. Debe tener entre 5 y 150 caracteres.'
        },
       },
       // Riesgos nivel producto
       "form2":{
        "descripcion2": {
            pattern: /^[\w\s.,?!;:'"()\-–—]{5,150}$/,
            errorMsg: 'La descripción no es válida. Debe tener entre 5 y 150 caracteres.'
        },
        "efectos2": {
            pattern: /^[\w\s.,?!;:'"()\-–—]{5,150}$/,
            errorMsg: 'Los efectos no son válidos. Debe tener entre 5 y 150 caracteres.'
        },
        "medidas_Mitigacion2": {
            pattern: /^[\w\s.,?!;:'"()\-–—]{5,150}$/,
            errorMsg: 'Las medidas de mitigación no son válidas. Debe tener entre 5 y 150 caracteres.'
        },
       },
    //Riesgos nivel actividades
       "form3":{
        "descripcion3": {
            pattern: /^[\w\s.,?!;:'"()\-–—]{5,150}$/,
            errorMsg: 'La descripción no es válida. Debe tener entre 5 y 150 caracteres.'
        },
        "efectos3": {
            pattern: /^[\w\s.,?!;:'"()\-–—]{5,150}$/,
            errorMsg: 'Los efectos no son válidos. Debe tener entre 5 y 150 caracteres.'
        },
        "medidas_Mitigacion3": {
            pattern: /^[\w\s.,?!;:'"()\-–—]{5,150}$/,
            errorMsg: 'Las medidas de mitigación no son válidas. Debe tener entre 5 y 150 caracteres.'
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
    const form3 = document.getElementById("form3");


    document.getElementById("enviar1").addEventListener("click", function() {
        handleFormSubmit(event, 'form1');
    });
    document.getElementById("enviar2").addEventListener("click", function() {
        handleFormSubmit(event, 'form2');
    });
    document.getElementById("enviar3").addEventListener("click", function() {
        handleFormSubmit(event, 'form3');
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
                    sendPost()
                }else if (formKey == 'form2'){
                    sendPost2()
                }else if(formKey == 'form3'){
                    sendPost3()
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

// Riesgo obj general
function sendPost() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    // Obtener los valores de los campos del formulario
    var tipo = document.getElementById("tipo").value;
    var descripcion = document.getElementById("descripcion").value;
    var probabilidad = document.getElementById("probabilidad").value;
    var impacto = document.getElementById("impacto").value;
    var medidas_Mitigacion = document.getElementById("medidas_Mitigacion").value;
    var efectos = document.getElementById("efectos").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("tipo", tipo);
    formData.append("descripcion", descripcion);
    formData.append("probabilidad", probabilidad);
    formData.append("impacto", impacto);
    formData.append("medidas_Mitigacion", medidas_Mitigacion);
    formData.append("efectos", efectos);
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/riesgos/riesgo-general/${id_proyecto}/`, {
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

// Riesgo productos
function sendPost2() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    // Obtener los valores de los campos del formulario
    var tipo = document.getElementById("tipo2").value;
    var descripcion = document.getElementById("descripcion2").value;
    var probabilidad = document.getElementById("probabilidad2").value;
    var impacto = document.getElementById("impacto2").value;
    var medidas_Mitigacion = document.getElementById("medidas_Mitigacion2").value;
    var efectos = document.getElementById("efectos2").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("tipo", tipo);
    formData.append("descripcion", descripcion);
    formData.append("probabilidad", probabilidad);
    formData.append("impacto", impacto);
    formData.append("medidas_Mitigacion", medidas_Mitigacion);
    formData.append("efectos", efectos);
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/riesgos/riesgo-producto/${id_proyecto}/`, {
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

// Riesgo actividad
function sendPost3() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    // Obtener los valores de los campos del formulario
    var tipo = document.getElementById("tipo3").value;
    var descripcion = document.getElementById("descripcion3").value;
    var probabilidad = document.getElementById("probabilidad3").value;
    var impacto = document.getElementById("impacto3").value;
    var medidas_Mitigacion = document.getElementById("medidas_Mitigacion3").value;
    var efectos = document.getElementById("efectos3").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("tipo", tipo);
    formData.append("descripcion", descripcion);
    formData.append("probabilidad", probabilidad);
    formData.append("impacto", impacto);
    formData.append("medidas_Mitigacion", medidas_Mitigacion);
    formData.append("efectos", efectos);
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/riesgos/riesgo-actividad/${id_proyecto}/`, {
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

