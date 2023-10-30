document.addEventListener("DOMContentLoaded", function() {
    
    const allValidations = {
        //Validacion info proponente
       "form1": {
        "nit": {
            pattern: /^\d{8,12}$/,
            errorMsg: 'El numero no es válido. Debe tener entre 6 y 12 caracteres'
        },
        "especifique_tipo_codigo_convenio": {
            pattern: /^[A-Za-z ]{5,100}$/,
            errorMsg: 'El correo no es válido. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        },
        "nombres_integrantes_participantes_entidad_aliada": {
            pattern: /^[A-Za-z ]{5,50}$/,
            errorMsg: 'El nombre no es válido debe llevar minimo 5 caracteres.',
        },
        "numero_identificacion_integrantes": {
            pattern: /^\d{8,12}$/,
            errorMsg: 'El nombre no es válido. Debe tener entre 5 y 50 caracteres y solo puede contener letras y espacios'
        },
        "email_integrantes": {
            pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
            errorMsg: 'El correo no es válido. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        },
        "numeros_celular_integrantes": {
            pattern: /^\d{10}$/,
            errorMsg: 'El número no es válido. Debe tener 10 digitos númericos',
        },
        "recursos_especie_entidad": {
            pattern: /^\d{10}$/,
            errorMsg: 'El nombre no es válido debe llevar minimo 5 caracteres.',
        },
        "descripcion_recursos_especie_aportados": {
            pattern: /^[A-Za-z ]{5,50}$/,
            errorMsg: 'El nombre no es válido debe llevar minimo 5 caracteres.',
        },
        "recursos_dinero_entidad_aliada": {
            pattern: /^[A-Za-z ]{5,50}$/,
            errorMsg: 'El nombre no es válido debe llevar minimo 5 caracteres.',
        },
        "descripcion_destinacion_dinero_aportado": {
            pattern: /^[A-Za-z ]{5,50}$/,
            errorMsg: 'El nombre no es válido debe llevar minimo 5 caracteres.',
        },
        "nombre_grupo_inv_entidad_aliada": {
            pattern: /^[A-Za-z ]{5,50}$/,
            errorMsg: 'El nombre no es válido debe llevar minimo 5 caracteres.',
        },
        "link_gruplac_entidad_aliada": {
            pattern: /^[A-Za-z ]{5,50}$/,
            errorMsg: 'El nombre no es válido debe llevar minimo 5 caracteres.',
        },
        "actividades_desarrollar_entidad_aliada_marco_proyecto": {
            pattern: /^[A-Za-z ]{5,50}$/,
            errorMsg: 'El nombre no es válido debe llevar minimo 5 caracteres.',
        },
        "objetivo_especificos_relacionados": {
            pattern: /^[A-Za-z ]{5,50}$/,
            errorMsg: 'El nombre no es válido debe llevar minimo 5 caracteres.',
        },
        "metodologia_act_transferencia_centro_formacion": {
            pattern: /^[A-Za-z ]{5,50}$/,
            errorMsg: 'El nombre no es válido debe llevar minimo 5 caracteres.',
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

    document.getElementById("enviar1").addEventListener("click", function(event) {
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
                if (formKey == 'form1'){
                    sendPost1()
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
}
);

function sendPost1() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    // Obtener los valores de los campos del formulario
    var nit = document.getElementById("nit").value;
    var especifique_tipo_codigo_convenio = document.getElementById("especifique_tipo_codigo_convenio").value;
    var nombres_integrantes_participantes_entidad_aliada = document.getElementById("nombres_integrantes_participantes_entidad_aliada").value;
    var numero_identificacion_integrantes = document.getElementById("numero_identificacion_integrantes").value;
    var email_integrantes = document.getElementById("email_integrantes").value;
    var numeros_celular_integrantes = document.getElementById("numeros_celular_integrantes").value;
    var recursos_especie_entidad = document.getElementById("recursos_especie_entidad").value;
    var descripcion_recursos_especie_aportados = document.getElementById("descripcion_recursos_especie_aportados").value;
    var recursos_dinero_entidad_aliada = document.getElementById("recursos_dinero_entidad_aliada").value;
    var descripcion_destinacion_dinero_aportado = document.getElementById("descripcion_destinacion_dinero_aportado").value;
    var nombre_grupo_inv_entidad_aliada = document.getElementById("nombre_grupo_inv_entidad_aliada").value;
    var link_gruplac_entidad_aliada = document.getElementById("link_gruplac_entidad_aliada").value;
    var actividades_desarrollar_entidad_aliada_marco_proyecto = document.getElementById("actividades_desarrollar_entidad_aliada_marco_proyecto").value;
    var objetivo_especificos_relacionados = document.getElementById("objetivo_especificos_relacionados").value;
    var metodologia_act_transferencia_centro_formacion = document.getElementById("metodologia_act_transferencia_centro_formacion").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("nit", nit);
    formData.append("especifique_tipo_codigo_convenio", especifique_tipo_codigo_convenio);
    formData.append("nombres_integrantes_participantes_entidad_aliada", nombres_integrantes_participantes_entidad_aliada);
    formData.append("numero_identificacion_integrantes", numero_identificacion_integrantes);
    formData.append("email_integrantes", email_integrantes);
    formData.append("numeros_celular_integrantes", numeros_celular_integrantes);
    formData.append("recursos_especie_entidad", recursos_especie_entidad);
    formData.append("descripcion_recursos_especie_aportados", descripcion_recursos_especie_aportados);
    formData.append("recursos_dinero_entidad_aliada", recursos_dinero_entidad_aliada);
    formData.append("descripcion_destinacion_dinero_aportado", descripcion_destinacion_dinero_aportado);
    formData.append("nombre_grupo_inv_entidad_aliada", nombre_grupo_inv_entidad_aliada);
    formData.append("link_gruplac_entidad_aliada", link_gruplac_entidad_aliada);
    formData.append("actividades_desarrollar_entidad_aliada_marco_proyecto", actividades_desarrollar_entidad_aliada_marco_proyecto);
    formData.append("objetivo_especificos_relacionados", objetivo_especificos_relacionados);
    formData.append("metodologia_act_transferencia_centro_formacion", metodologia_act_transferencia_centro_formacion);
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/info-proyecto/centro_formacion/${id_proyecto}/`, {
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
