const button1 = document.getElementById('step2');

const collapse1 = document.getElementById('collapseOne');
const collapse2 = document.getElementById('collapseTwo');

selectTipo = document.getElementById('select_box')
selectRubro = document.getElementById('select_box2')
buttonsDiv = document.querySelectorAll('.dselect-items')
botones = buttonsDiv[1].getElementsByTagName('button')

selectTipo.addEventListener('change', function() {
    for (var i = 1; i < selectRubro.options.length; i++){
        if (selectRubro.options[i].getAttribute("data-Asociacion") !== selectTipo.value){
            botones[i].style.display = 'none'
        }else{
            botones[i].style.display = 'block';
        }
    }
})

document.addEventListener("DOMContentLoaded", function() {
    
    const allValidations = {
        //Estructura del proyecto
       "form1": {
        "actividad": {
            pattern: /^.{1,1000}$/,
            errorMsg: 'Seleccione un objetivo especifico por favor.'
        },
        "fecha_inicio": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{5,250}$/,
            errorMsg: 'La fecha no es válida. Por favor ingresela nuevamente.'
        },
        "fecha_cierre": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{5,250}$/,
            errorMsg: 'La fecha no es válida. Por favor ingresela nuevamente.'
        },
        "observacion": {
            pattern: /^[\w\s.,?!;:'"()\-–—¿¡=ÑñA-Za-záéíóúÁÉÍÓÚ, .#$%&[\]/]{5,250}$/,
            errorMsg: 'La fecha no es válida. Por favor ingresela nuevamente.'
        }
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


    document.getElementById("enviar1").addEventListener("click", function() {
        handleFormSubmit(event, 'form1');
    });
    document.getElementById("enviar2").addEventListener("click", function() {
        handleFormSubmit(event, 'form2');
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
                    sendPost1()
                    button1.setAttribute('aria-expanded', (button1.getAttribute('aria-expanded') === 'true') ? 'false' : 'true');
                    progress.setAttribute('value', 1 * 100 / (stepButtons.length - 1));
                    collapse1.classList.remove('show')
                    collapse2.classList.add('show')
                }else if (formKey == 'form2'){
                    sendPost2()
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

function sendPost1() {    
    var id_proyecto = document.getElementById("id_proyecto").value;

    const actorEntidades = [];
    const actorPartipantes = [];

    let i = 1;
    while (true) {
        const actorEntidad = document.getElementById(`entidad${i}`);
        if (actorEntidad) {
            actorEntidades.push(actorEntidad.checked);
            console.log(`Entidad ${i}:`, actorEntidad.checked);
        } else {
            break;
        }
        i++;
    }

    i = 1;
    while (true) {
        const actorPartipante = document.getElementById(`participante${i}`);
        if (actorPartipante) {
            actorPartipantes.push(actorPartipante.checked);
            console.log(`Participante ${i}:`, actorPartipante.checked);
        } else {
            break;
        }
        
        i++;
    }

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    var actividad = document.getElementById("actividad").value
    formData.append("actividad", actividad);
    formData.append("fch_inicio", document.getElementById("fecha_inicio").value);
    formData.append("fch_cierre", document.getElementById("fecha_cierre").value);
    formData.append("observacion", document.getElementById("observacion").value);
    formData.append("actorEntidad", JSON.stringify(actorEntidades));
    formData.append("actorPartipantes", JSON.stringify(actorPartipantes));
    formData.append("csrfmiddlewaretoken", document.querySelector('[name=csrfmiddlewaretoken]').value);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/${id_proyecto}/recursos/cronograma/${actividad}/`, {
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

function sendPost2() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    var actividad = document.getElementById("actividadR").value

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("actividadR", actividad);
    formData.append("tipo_rubro", document.getElementById("select_box").value);
    formData.append("valor", document.getElementById("valor").value);
    formData.append("rubro", document.getElementById("select_box2").value);
    formData.append("csrfmiddlewaretoken", document.querySelector('[name=csrfmiddlewaretoken]').value);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/${id_proyecto}/recursos/presupuesto/${actividad}/`, {
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