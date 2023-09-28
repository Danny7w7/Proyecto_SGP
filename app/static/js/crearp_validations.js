
document.addEventListener("DOMContentLoaded", function() {
    
    const validations = {
        "titulo_Proyecto": {
            pattern: /^[A-Za-z0-9 ,.]{5,100}$/,
            errorMsg: 'El título no es válido. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        },
        "descripcion": {
            pattern: /^[A-Za-z0-9 ,.]{5,100}$/,
            errorMsg: 'La descripción no es válida. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        }
    };

    for (let fieldId in validations) {
        const inputField = document.getElementById(fieldId);
        const feedbackElement = inputField.nextElementSibling;
        const { pattern, errorMsg } = validations[fieldId];

        inputField.addEventListener("input", function() {
            validateField(inputField, feedbackElement, pattern, errorMsg);
        });
    }

    document.querySelector("form").addEventListener("submit", function(event) {
        let isValid = true;
        for (let fieldId in validations) {
            const inputField = document.getElementById(fieldId);
            const feedbackElement = inputField.nextElementSibling;
            const { pattern, errorMsg } = validations[fieldId];
            isValid = validateField(inputField, feedbackElement, pattern, errorMsg) && isValid;
        }

        event.preventDefault();

        if (isValid) {
            Swal.fire({
                title: '¡Éxito!',
                text: 'Información registrada correctamente.',
                icon: 'success',
                confirmButtonText: 'Aceptar'
            });
        } else {
            Swal.fire({
                title: 'Error!',
                text: 'Por favor, corrija los errores en el formulario antes de enviar.',
                icon: 'error',
                confirmButtonText: 'Aceptar'
            });
        }
    });

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
