document.addEventListener("DOMContentLoaded", function() {
    const allValidations = {
        //Estructura del proyecto
       "form1": {
        "desc_resultado_esperado": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{1,3000}$/,
            errorMsg: 'La descripcion no es válida. Debe tener entre 5 y 3000 caracteres y no puede contener caracteres especiales'
        },
        "nombre_resul_investigacion": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{1,300}$/,
            errorMsg: 'El nombre no es válido. Debe tener entre 5 y 300 caracteres y no puede contener caracteres especiales'
        },
        "indicador_producto_resultado_inv_obj_especifico": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&()+*==$><|°[\]/]{1,300}$/,
            errorMsg: 'El indicador no es válido. Debe tener entre 5 y 300 caracteres y no puede contener caracteres especiales'
        },
        "fch_entrega_producto_resultado_inv_obj_especifico": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{1,300}$/,
            errorMsg: 'Por favor seleccione una fecha.'
        },
        "tipo_resultado_esperado_obj_especifico": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{1,300}$/,
            errorMsg: 'Por favor seleccione una opcion.'
        },
        "trl_producto_resultado_inv_obj_especifico": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{1,300}$/,
            errorMsg: 'Por favor seleccione una opcion.'
        },
        "nombre_subtipologia": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{1,300}$/,
            errorMsg: 'Por favor seleccione una opcion.'
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
                form1.submit();
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