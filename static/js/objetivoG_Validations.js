let conjuntosMostrados = 1;
function mostrarDivs() {
  // Mostrar conjuntos adicionales solo si no se han mostrado más de 2
  if (conjuntosMostrados < 2) {
    document.querySelector('.la_prueba2').style.display = 'block';
    conjuntosMostrados++;
  } else if(conjuntosMostrados == 2) {
    document.querySelector('.la_prueba3').style.display = 'block';
    conjuntosMostrados++;
  } else{
    alert('Solo puedes crear 3 objetivos especificos por proyecto.')
  }
}
document.addEventListener("DOMContentLoaded", function() {
    const allValidations = {
        //Estructura del proyecto
       "form1": {
        "objetivo_general": {
            pattern: /^[\s\S]{5,300}$/,
            errorMsg: 'El obj general no es válido. Debe tener entre 5 y 300 caracteres y no puede contener caracteres especiales'
        },
        "objetivo_especifico1": {
            pattern: /^[\s\S]{5,300}$/,
            errorMsg: 'El obj especifico no es válido. Debe tener entre 5 y 300 caracteres y no puede contener caracteres especiales'
        },
        // "objetivo_especifico2": {
        //     pattern: /^[\s\S]{5,300}$/,
        //     errorMsg: 'El obj especifico no es válido. Debe tener entre 5 y 300 caracteres y no puede contener caracteres especiales'
        // },
        // "objetivo_especifico3": {
        //     pattern: /^[\s\S]{5,300}$/,
        //     errorMsg: 'El obj especifico no es válido. Debe tener entre 5 y 300 caracteres y no puede contener caracteres especiales'
        // }
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
                let senduwu = false;
                validateField(inputField, feedbackElement, pattern, errorMsg);
            });
        }
    }

//ids de los formularios
    const form1 = document.getElementById("form1");


    document.getElementById("enviar1").addEventListener("click", function() {
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
                sendPost1();
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
    var id_proyecto = document.getElementById('id_proyecto').value;
    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("objetivo_general", document.getElementById("objetivo_general").value);
    if (!(document.getElementById('objetivo_especifico1').value == '')){
        formData.append("objetivo_especifico1", document.getElementById('objetivo_especifico1').value);
    }if (!(document.getElementById('objetivo_especifico2').value == '')){
        formData.append("objetivo_especifico2", document.getElementById('objetivo_especifico2').value);
    }if (!(document.getElementById('objetivo_especifico3').value == '')){
        formData.append("objetivo_especifico3", document.getElementById('objetivo_especifico3').value);
    }
    formData.append("csrfmiddlewaretoken", document.querySelector('[name=csrfmiddlewaretoken]').value);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/arbol-problemas/objetivos/${id_proyecto}/`, {
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
    // .catch(error => {
    //     console.error('Error en la solicitud:', error);
    //     // Manejar errores en la solicitud, como problemas de red
    // });
};