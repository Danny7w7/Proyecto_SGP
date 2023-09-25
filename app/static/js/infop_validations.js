
document.addEventListener("DOMContentLoaded", function() {
    
    const allValidations = {
        //Validacion info proponente
       "form1": {
        "Nombre_Director": {
            pattern: /^[A-Za-z ]{5,50}$/,
            errorMsg: 'El nombre no es válido. Debe tener entre 5 y 50 caracteres y solo puede contener letras y espacios'
        },
        "email_director": {
            pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
            errorMsg: 'El correo no es válido. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        },
        "Numero_Director": {
            pattern: /^\d{10}$/,
            errorMsg: 'El número no es válido. Debe tener 10 digitos númericos',
        },
        "Nombre_Sub_Director": {
            pattern: /^[A-Za-z ]{5,50}$/,
            errorMsg: 'El nombre no es válido. Debe tener entre 5 y 50 caracteres y solo puede contener letras y espacios'
        },
        "email_sub_director": {
            pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
            errorMsg: 'El correo no es válido. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        },
        "Numero_Sub_Director": {
            pattern: /^\d{10}$/,
            errorMsg: 'El número no es válido. Debe tener 10 digitos númericos',
        },
       },
       // Validacion autor
       "form2":{
        "Nombre_Autor_Proyecto": {
            pattern: /^[A-Za-z ]{5,50}$/,
            errorMsg: 'El nombre no es válido. Debe tener entre 5 y 50 caracteres y solo puede contener letras y espacios'
        },
        "Numero_Cedula_Autor": {
            pattern: /^\d{10}$/,
            errorMsg: 'El número de documento no es válido. Debe tener 10 digitos númericos',
        },
        "Email_Autor_Proyecto": {
            pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
            errorMsg: 'El correo no es válido. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        },
        "Numero_meses_vinculacion_Autor": {
            pattern: /^\d{1,2}$/,
            errorMsg: 'El número no es válido. Debe tener digitos númericos',
        },
        "Numero_Telefono_Autor": {
            pattern: /^\d{10}$/,
            errorMsg: 'El número no es válido. Debe tener 10 digitos númericos',
        },
        "Numero_horas_Semanales_dedicadas_Autores": {
            pattern: /^(0|[1-9]\d?|1[0-6]\d|168)$/,
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
    const form2 = document.getElementById("form2");

    if(form1) {
        form1.addEventListener("submit", function(event) {
            handleFormSubmit(event, 'form1');
        });
    }

    if(form2) {
        form2.addEventListener("submit", function(event) {
            handleFormSubmit(event, 'form2');
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

        if (!isValid) {
            event.preventDefault();
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
