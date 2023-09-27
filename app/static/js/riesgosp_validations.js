
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
