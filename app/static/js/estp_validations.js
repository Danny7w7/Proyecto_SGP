
document.addEventListener("DOMContentLoaded", function() {
    
    const allValidations = {
        //Estructura del proyecto
       "form1": {
        "resumen_ejecutivo": {
            pattern: /^[\w\s.,?!;:'"()\-–—]{5,250}$/,
            errorMsg: 'El resumen no es válido. Debe tener entre 5 y 250 caracteres.'
        },
        "antecedentes": {
            pattern: /^[\w\s.,?!;:'"()\-–—]{5,250}$/,
            errorMsg: 'El resumen no es válido. Debe tener entre 5 y 250 caracteres.'
        },
       },
       // Arbol de problemas(por definir)
    //    "form2":{
    //     "arbol_de_problemas": {
    //         pattern: /^[\w\s.,?!;:'"()\-–—]{5,250}$/,
    //         errorMsg: 'Identificación y descripción no es válido. Debe tener entre 5 y 250 caracteres.'
    //     },
    //    },

    //Descripcion del problema
       "form3":{
        "identificacion_y_descripcion_problema": {
            pattern: /^[\w\s.,?!;:'"()\-–—]{5,250}$/,
            errorMsg: 'Identificación y descripción no es válido. Debe tener entre 5 y 250 caracteres.'
        },
        "justificacion": {
            pattern: /^[\w\s.,?!;:'"()\-–—]{5,250}$/,
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
    // const form2 = document.getElementById("form2");
    const form3 = document.getElementById("form3");


    if(form1) {
        form1.addEventListener("submit", function(event) {
            handleFormSubmit(event, 'form1');
        });
    }

    // if(form2) {
    //     form2.addEventListener("submit", function(event) {
    //         handleFormSubmit(event, 'form2');
    //     });
    // }
    if (form3) {
        form3.addEventListener("submit", function(event) {
            handleFormSubmit(event, 'form3');
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
