
document.addEventListener("DOMContentLoaded", function() {
    
    const allValidations = {
        //Estructura del proyecto
       "form1": {
        "titulo_Proyecto": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{5,200}$/,
            errorMsg: 'El titulo del proyecto no es válido. Debe tener entre 5 y 200 caracteres y no puede contener caracteres especiales'
        },
        "descripcion": {
            pattern:  /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{5,500}$/,
            errorMsg: 'La descripción no es válida. Debe tener entre 5 y 500 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        },
    }
}

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


    if(form1) {
        form1.addEventListener("submit", function(event) {
            handleFormSubmit(event, 'form1');
        });
    }


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
                // Esto enviará realmente el formulario
                event.target.submit();
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
