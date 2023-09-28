
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
            pattern: /^\d{5,20}$/,
            errorMsg: 'El número de documento no es válido. Debe tener digitos númericos',
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
            errorMsg: 'El número no es válido. Debe tener digitos númericos',
        },
       },
    //    //Validacion participantes
       "form3":{
        "Nombre_participantes_de_desarrollo":{
            pattern: /^[A-Za-z ]{5,50}$/,
            errorMsg: 'El nombre no es válido. Debe tener entre 5 y 50 caracteres y solo puede contener letras y espacios',
        }, 
        "Numero_cedula_participantes": {
            pattern: /^\d{5,20}$/,
            errorMsg: 'El número de documento no es válido. Debe tener digitos númericos',
        },
        "Numero_meses_vinculacion_participantes": {
            pattern: /^\d{1,2}$/,
            errorMsg: 'El número no es válido. Debe tener digitos númericos',
        },
        "Email_participantes_de_desarrollo": {
            pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
            errorMsg: 'El correo no es válido. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        },
        "Numero_horas_Semanales_dedicadas_participantes": {
            pattern: /^(0|[1-9]\d?|1[0-6]\d|168)$/,
            errorMsg: 'El número no es válido. Debe tener digitos númericos',
        },
        "Numero_Telefono_participantes": {
            pattern: /^\d{10}$/,
            errorMsg: 'El número no es válido. Debe tener 10 digitos númericos',
        },
       },
       "form4":{
        "Numero_Telefono_participantes": {
            pattern: /^\d{10}$/,
            errorMsg: 'El link no es válido.',
        },
        "link_video_proyecto": {
            pattern: /^(http|https):\/\/[^ "]+$/,
            errorMsg: 'El link no es válido.',
        },
        "justificacion_Economia_Naranja":{
            pattern: /^[A-Za-z ]{5,500}$/,
            errorMsg: 'La justificación no es válida. Debe tener entre 5 y 500 caracteres y solo puede contener letras y espacios',
        }, 
        "justificacion_Politica_Discapacidad":{
            pattern: /^[A-Za-z ]{5,500}$/,
            errorMsg: 'La justificación no es válida. Debe tener entre 5 y 500 caracteres y solo puede contener letras y espacios',
        }, 
        "justificacion_Industrial":{
            pattern: /^[A-Za-z ]{5,500}$/,
            errorMsg: 'La justificación no es válida. Debe tener entre 5 y 500 caracteres y solo puede contener letras y espacios',
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
    const form3 = document.getElementById("form3");
    const form4 = document.getElementById("form4");

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
    if (form3) {
        form3.addEventListener("submit", function(event) {
            handleFormSubmit(event, 'form3');
        });
    }
    if (form4) {
        form4.addEventListener("submit", function(event) {
            handleFormSubmit(event, 'form4');
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
