let conjuntosMostrados = 1;
fieldExclude2 = ['id_objetivo_especificos2', 'id_actividad2' ,'id_causa2', 'id_efecto2']
fieldExclude3 = ['id_objetivo_especificos3','id_actividad3', 'id_causa3', 'id_efecto3']
function mostrarDivs() {
  // Mostrar conjuntos adicionales solo si no se han mostrado más de 2
  if (conjuntosMostrados < 2) {
    document.querySelector('.la_prueba2').style.display = 'block';
    conjuntosMostrados++;
  } else {
    document.querySelector('.la_prueba3').style.display = 'block';
    conjuntosMostrados++;
  }
}
document.addEventListener("DOMContentLoaded", function() {
    const allValidations = {
        //Estructura del proyecto
       "form1": {
        "id_objetivo_general": {
            pattern: /^[\s\S]{5,500}$/,
            errorMsg: 'El obj general no es válido. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales'
        },
        "id_objetivo_especificos": {
            pattern: /^[\s\S]{5,500}$/,
            errorMsg: 'El obj especifico no es válido. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales'
        },
        "id_actividad": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{1,3000}$/,
            errorMsg: 'El resumen no es válido. Debe tener entre 5 y 3000 caracteres y no puede contener caracteres especiales'
        },
        "id_causa": {
            pattern: /^[\s\S]{5,500}$/,
            errorMsg: 'La  causa no es válida. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales'
        },
        "id_efecto": {
            pattern: /^[\s\S]{5,500}$/,
            errorMsg: 'El efecto no es válido. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales'
        },
        "id_objetivo_especificos2": {
            pattern: /^[\s\S]{5,500}$/,
            errorMsg: 'El obj especifico 2 no es válido. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales'
        },
        "id_actividad2": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{1,3000}$/,
            errorMsg: 'El resumen no es válido. Debe tener entre 5 y 3000 caracteres y no puede contener caracteres especiales'
        },
        "id_causa2": {
            pattern: /^[\s\S]{5,500}$/,
            errorMsg: 'La causa 2 no es válida. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales'
        },
        "id_efecto2": {
            pattern: /^[\s\S]{5,500}$/,
            errorMsg: 'El efecto 2 no es válido. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales'
        },
        "id_objetivo_especificos3": {
            pattern: /^[\s\S]{5,500}$/,
            errorMsg: 'El obj especifico 3 no es válido. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales'
        },
        "id_actividad3": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{1,3000}$/,
            errorMsg: 'El resumen no es válido. Debe tener entre 5 y 3000 caracteres y no puede contener caracteres especiales'
        },
        "id_causa3": {
            pattern: /^[\s\S]{5,500}$/,
            errorMsg: 'La causa 3 no es válida. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales'
        },
        "id_efecto3": {
            pattern: /^[\s\S]{5,500}$/,
            errorMsg: 'El efecto 3 no es válido. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales'
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
            
            let senduwu = true;
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
        if (conjuntosMostrados == 1){
            var index2 = fieldExclude2.indexOf(field.id);
            var index3 = fieldExclude3.indexOf(field.id);
            if (index2 > -1 || index3 > -1){   
                field.classList.remove("is-invalid");
                field.classList.add("is-valid");
                feedback.textContent = '';
                console.log(`El campo ${field.id} No se cambio`)
                return true;
            }
        }else if (conjuntosMostrados == 2){
            var index3 = fieldExclude3.indexOf(field.id);
            if (index3 > -1){   
                field.classList.remove("is-invalid");
                field.classList.add("is-valid");
                feedback.textContent = '';
                console.log(`El campo ${field.id} No se cambio`)
                return true;
            }
        }
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