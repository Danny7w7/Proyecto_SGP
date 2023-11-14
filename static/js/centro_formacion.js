document.addEventListener("DOMContentLoaded", function() {
    
    const allValidations = {
        "form1": {
            "nombre_semillero_investigacion_beneficiados": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,100}$/u,
                errorMsg: 'El nombre no es válido. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
            },
            "nombre_programas_formacion_beneficiados_semillero": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,100}$/u,
                errorMsg: 'El nombre no es válido. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
            },
            "nombre_programas_formacion_beneficiados_ejecucion_proyecto": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,100}$/u,
                errorMsg: 'El nombre no es válido. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
            },
            "numero_aprendices_participaran_ejecución_proyecto": {
                pattern: /^\d{1}$/,
                errorMsg: 'El numero no es válido.'
            },
            "numero_municipios_beneficiados": {
                pattern: /^\d{1,5}$/,
                errorMsg: 'El número no es válido.'
            },
            "nombre_municipios_beneficiados_descripcion_beneficio": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,200}$/u,
                errorMsg: 'El nombre no es válido.',
            },
            "numero_aprendices_participaran_ejecucion_proyecto": {
                pattern: /^\d{1,}$/,
                errorMsg: 'El número no es válido.',
            }
           },
        "form2": {
            "nombre_entidad": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,200}$/u,
                errorMsg: 'El nombre no es válido. Debe tener entre 5 y 200 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
            },
            "nit": {
                pattern: /^\d{6,12}$/,
                errorMsg: 'El numero no es válido. Debe tener entre 6 y 12 caracteres'
            },
            "especifique_tipo_codigo_convenio": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,100}$/u,
                errorMsg: 'El nómbre no es válido. Debe tener entre 5 y 100 caracteres.'
            },
            "nombres_integrantes_participantes_entidad_aliada": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,100}$/u,
                errorMsg: 'El nombre no es válido. Debe tener entre 5 y 200 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
            },
            "numero_identificacion_integrantes": {
                pattern: /^\d{8,12}$/,
                errorMsg: 'El número no es válido. Debe tener entre 5 y 12 caracteres y solo puede contener números'
            },
            "email_integrantes": {
                pattern: /^[a-zA-Z0-9._%+-ñÑ,]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
                errorMsg: 'El correo no es válido. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
            },
            "numeros_celular_integrantes": {
                pattern: /^\d{10}$/,
                errorMsg: 'El número no es válido. Debe tener 10 digitos númericos',
            },
            "recursos_especie_entidad": {
                pattern: /^\d{5,10}$/,
                errorMsg: 'El número no es válido debe llevar minimo 5 caracteres.',
            },
            "descripcion_recursos_especie_aportados": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,150}$/u,
                errorMsg: 'El nombre no es válido debe llevar minimo 5 y 150 caracteres.',
            },
            "recursos_dinero_entidad_aliada": {
                pattern: /^\d{5,10}$/,
                errorMsg: 'El número no es válido debe llevar minimo 5 caracteres.',
            },
            "descripcion_destinacion_dinero_aportado": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,150}$/u,
                errorMsg: 'El nombre no es válido debe llevar minimo 5 y 150 caracteres.',
            },
            "nombre_grupo_inv_entidad_aliada": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,170}$/u,
                errorMsg: 'El nombre no es válido debe llevar minimo 5 y 170 caracteres.',
            },
            "link_gruplac_entidad_aliada": {
                pattern: /^[A-Za-z ]{5,50}$/,
                errorMsg: 'El nombre no es válido debe llevar minimo 5 caracteres.',
            },
            "actividades_desarrollar_entidad_aliada_marco_proyecto": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,250}$/u,
                errorMsg: 'El nombre no es válido debe llevar minimo 5 y 250 caracteres.',
            },
            "objetivo_especificos_relacionados": {
                pattern: /^[A-Za-z ]{5,250}$/,
                errorMsg: 'El nombre no es válido debe llevar minimo 5 y 250 caracteres.',
            },
            "metodologia_act_transferencia_centro_formacion": {
                pattern: /^[A-Za-z ]{5,250}$/,
                errorMsg: 'El nombre no es válido debe llevar minimo 5 y 250 caracteres.',
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


    document.getElementById("enviar1").addEventListener("click", function(event) {
        handleFormSubmit(event, 'form1');
    });
    
    document.getElementById("enviar2").addEventListener("click", function(event) {
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
                }else if(formKey == 'form2'){
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


// Centro de formacion
function sendPost1() {
    // Obtén el id del proyecto
    var id_proyecto = document.getElementById('id_proyecto').value;

    // Obtén los datos del formulario
    var nombre_semillero_investigacion_beneficiados = document.getElementById("nombre_semillero_investigacion_beneficiados").value;
    var numero_programas_beneficiarios_semilleros_investigacion = document.getElementById("numero_programas_beneficiarios_semilleros_investigacion").value;
    var tipo_programas_formacion_beneficiados_conforman_semillero = document.getElementById("tipo_programas_formacion_beneficiados_conforman_semillero").value;
    var nombre_programas_formacion_beneficiados_semillero = document.getElementById("nombre_programas_formacion_beneficiados_semillero").value;
    var tipo_programas_de_formacion_beneficiados_por_ejecucion = document.getElementById("tipo_programas_de_formacion_beneficiados_por_ejecucion").value;
    var nombre_programas_formacion_beneficiados_ejecucion_proyecto = document.getElementById("nombre_programas_formacion_beneficiados_ejecucion_proyecto").value;
    var numero_aprendices_participaran_ejecucion_proyecto = document.getElementById("numero_aprendices_participaran_ejecucion_proyecto").value;
    var numero_municipios_beneficiados = document.getElementById("numero_municipios_beneficiados").value;
    var nombre_municipios_beneficiados_descripcion_beneficio = document.getElementById("nombre_municipios_beneficiados_descripcion_beneficio").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Crear un objeto FormData para los datos del formulario
var formData = new FormData();
formData.append("nombre_semillero_investigacion_beneficiados",nombre_semillero_investigacion_beneficiados);
formData.append("numero_programas_beneficiarios_semilleros_investigacion", numero_programas_beneficiarios_semilleros_investigacion);
formData.append("tipo_programas_formacion_beneficiados_conforman_semillero", tipo_programas_formacion_beneficiados_conforman_semillero);
formData.append("nombre_programas_formacion_beneficiados_semillero", nombre_programas_formacion_beneficiados_semillero);
formData.append("tipo_programas_de_formacion_beneficiados_por_ejecucion", tipo_programas_de_formacion_beneficiados_por_ejecucion);
formData.append("nombre_programas_formacion_beneficiados_ejecucion_proyecto", nombre_programas_formacion_beneficiados_ejecucion_proyecto);
formData.append("numero_aprendices_participaran_ejecucion_proyecto", numero_aprendices_participaran_ejecucion_proyecto);
formData.append("numero_municipios_beneficiados", numero_municipios_beneficiados);
formData.append("nombre_municipios_beneficiados_descripcion_beneficio", nombre_municipios_beneficiados_descripcion_beneficio);
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

// Entidad aliada
function sendPost2() {
    // Obtén el id del proyecto
    var id_proyecto = document.getElementById('id_proyecto').value;

    // Obtén los datos del formulario
    var nombre_entidad = document.getElementById("nombre_entidad").value;
    var tipo_entidad = document.getElementById("tipo_entidad_aliada").value;
    var naturaleza_entidad = document.getElementById("naturaleza_entidad").value;
    var clasificacion_empresa = document.getElementById("clasificacion_empresa").value;
    var nit = document.getElementById("nit").value;
    var convenio = document.getElementById("convenio").value;
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
    var codigo_gruplac_entidad_aliada = document.getElementById("codigo_gruplac_entidad_aliada").value;
    var link_gruplac_entidad_aliada = document.getElementById("link_gruplac_entidad_aliada").value;
    var actividades_desarrollar_entidad_aliada_marco_proyecto = document.getElementById("actividades_desarrollar_entidad_aliada_marco_proyecto").value;
    var objetivo_especificos_relacionados = document.getElementById("objetivo_especificos_relacionados").value;
    var metodologia_act_transferencia_centro_formacion = document.getElementById("metodologia_act_transferencia_centro_formacion").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Crear un objeto FormData para los datos del formulario
var formData = new FormData();
formData.append("nombre_entidad",nombre_entidad);
formData.append("tipo_entidad_aliada", tipo_entidad);
formData.append("naturaleza_entidad", naturaleza_entidad);
formData.append("clasificacion_empresa", clasificacion_empresa);
formData.append("nit", nit);
formData.append("convenio", convenio);
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
formData.append("codigo_gruplac_entidad_aliada", codigo_gruplac_entidad_aliada);
formData.append("link_gruplac_entidad_aliada", link_gruplac_entidad_aliada);
formData.append("actividades_desarrollar_entidad_aliada_marco_proyecto", actividades_desarrollar_entidad_aliada_marco_proyecto);
formData.append("objetivo_especificos_relacionados", objetivo_especificos_relacionados);
formData.append("metodologia_act_transferencia_centro_formacion", metodologia_act_transferencia_centro_formacion);
formData.append("csrfmiddlewaretoken", csrfToken);
// Realizar una solicitud POST utilizando Fetch
fetch(`/proyecto/info-proyecto/entidad_aliada/${id_proyecto}/`, {
    method: 'POST',
    body: formData,
})
.then(response => response.json())  // Parsea la respuesta JSON
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
            alert(data.error); // O muestra el error de alguna otra manera
        } else {
            console.log('Mensaje de éxito:', data.mensaje);
            
            // Aquí, puedes agregar el nuevo autor a la tabla
            let tableBody = document.querySelector('.tablita tbody');
            let newRow = tableBody.insertRow();
            
            newRow.insertCell(0).textContent = data.nueva_entidad.nombre_entidad;
            newRow.insertCell(1).textContent = data.nueva_entidad.tipo_entidad_aliada;
            newRow.insertCell(2).textContent = data.nueva_entidad.naturaleza_entidad;
            newRow.insertCell(3).textContent = data.nueva_entidad.clasificacion_empresa;
            newRow.insertCell(4).textContent = data.nueva_entidad.nit;
    
            let actionsCell = newRow.insertCell(5);
            let actionDiv = document.createElement('div');
            actionDiv.className = "d-flex";
            
            let editButton = document.createElement('button');
            editButton.className = "btn btn-sm btn-outline-primary me-2";
            editButton.textContent = "Editar";
            // Aquí puedes añadir eventos al botón editar si lo necesitas
            
            let deleteButton = document.createElement('button');
            deleteButton.className = "btn btn-sm btn-outline-danger";
            deleteButton.textContent = "Eliminar";
            // Aquí puedes añadir eventos al botón eliminar si lo necesitas
    
            actionDiv.appendChild(editButton);
            actionDiv.appendChild(deleteButton);
            actionsCell.appendChild(actionDiv);
        }
    })
    .catch(error => {
        console.error('Error en la solicitud:', error);
        // Manejar errores en la solicitud, como problemas de red
    });
};

