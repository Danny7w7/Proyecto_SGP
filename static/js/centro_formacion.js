const button1 = document.getElementById('step2');

const collapse1 = document.getElementById('collapseOne');
const collapse2 = document.getElementById('collapseTwo');

function edit_entidad(id){
    const selectDiv = document.getElementById(`entidad${id}`);
    const inputs = selectDiv.querySelectorAll('input[type="hidden"]');

    for (let i = 0; i < inputs.length; i++) {
        let texto = inputs[i].id;
        texto = texto.substring(0, texto.length - 7);
        const changeDiv = document.getElementById(texto);
        changeDiv.value = inputs[i].value
    }


    var id_entidad = document.getElementById('id_entidad').value;
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/getEntidad/${id_entidad}/`, {
        method: 'POST',
    })
    .then(response => response.json())  // Parsea la respuesta JSON
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
        } else {
            console.log('Mensaje de éxito:', data.mensaje);

            const idsObjetivos = data.id_objetivos_asociados.id.map(obj => obj.id);

            objEspecificos = document.getElementsByClassName(`objEspecifico`)
            for (let i = 0; i < objEspecificos.length; i++){
                let textoSinPrimerasLetras = objEspecificos[i].id.substring(13);
                if (idsObjetivos.includes(parseInt(textoSinPrimerasLetras))) {
                    objEspecificos[i].checked = true
                } else {
                    objEspecificos[i].checked = false
                }
                
            }
            if (data.id == document.getElementById('id_entidad').length - 7){
                
            }
        }
    })
}


document.addEventListener("DOMContentLoaded", function() {
    fieldQuestion = ['convenio']
    fieldExclude = ['especifique_tipo_codigo_convenio']
    var inputs = fieldQuestion.map(function(id) {
        return document.getElementById(id);
    });

    var id_proyecto = document.getElementById('id_proyecto').value;
    
    const allValidations = {
        "form1": {
            "nombre_semillero_investigacion_beneficiados": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{5,300}$/u,
                errorMsg: 'El nombre no es válido. Debe tener entre 5 y 300 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
            },
            "nombre_programas_formacion_beneficiados_semillero": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{5,300}$/u,
                errorMsg: 'El nombre del programa no es válido. Debe tener entre 5 y 300 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
            },
            "nombre_programas_formacion_beneficiados_ejecucion_proyecto": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{5,300}$/u,
                errorMsg: 'El nombre del programa no es válido. Debe tener entre 5 y 300 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
            },
            "numero_aprendices_participaran_ejecucion_proyecto": {
                pattern: /^\d{1}$/,
                errorMsg: 'El número de aprendices no es válido.'
            },
            "numero_municipios_beneficiados": {
                pattern: /^\d{1,5}$/,
                errorMsg: 'El número de municipios no es válido.'
            },
            "nombre_municipios_beneficiados_descripcion_beneficio": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{4,200}$/u,
                errorMsg: 'El nombre de los municipios no son válidos.',
            },
            "numero_aprendices_participaran_ejecucion_proyecto": {
                pattern: /^\d{1,}$/,
                errorMsg: 'El número no es válido.',
            }
           },
        "form2": {
            "nombre_entidad": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{5,200}$/u,
                errorMsg: 'El nombre de la entidad no es válido. Debe tener entre 5 y 200 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
            },
            "nit": {
                pattern: /^\d{5,20}-\d{1}$/u,
                errorMsg: 'El nit no es válido. Debe tener entre 6 y 12 caracteres'
            },
            "especifique_tipo_codigo_convenio": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{5,50}$/u,
                errorMsg: 'El tipo y código de convenio no es válido. Debe tener entre 5 y 50 caracteres.'
            },
            "recursos_especie_entidad": {
                pattern: /^(0|[1-9]\d{4,8}|1000000000)$/,
                errorMsg: 'El número de recursos en especie no es válido debe llevar máximo una cifra de 1.000 millones.',
            },
            "descripcion_recursos_especie_aportados": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{5,150}$/u,
                errorMsg: 'La descripción del recurso no es válido debe llevar minimo 5 y 150 caracteres.',
            },
            "recursos_dinero_entidad_aliada": {
                pattern: /^(0|[1-9]\d{4,8}|1000000000)$/,
                errorMsg: 'El número de recursos en dinero no es válido debe contener máximo una cifra de 1.000 millones.',
            },
            "descripcion_destinacion_dinero_aportado": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{5,150}$/u,
                errorMsg: 'El nombre no es válido debe llevar minimo 5 y 150 caracteres.',
            },
            "nombre_grupo_inv_entidad_aliada": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,170}$/u,
                errorMsg: 'El nombre no es válido debe llevar minimo 5 y 170 caracteres.',
            },
            "link_gruplac_entidad_aliada": {
                pattern: /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/,
                errorMsg: 'El nombre no es válido debe llevar minimo 5 caracteres.',
            },
            "actividades_desarrollar_entidad_aliada_marco_proyecto": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/]{5,1500}$/u,
                errorMsg: 'El nombre no es válido debe llevar minimo 5 y 250 caracteres.',
            },
            "metodologia_act_transferencia_centro_formacion": {
                pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s!?¿¡'"_+#\-%&[\]:;{}\/()+*==$><|°]{5,8000}$/u,
                errorMsg: 'El nombre no es válido debe llevar minimo 5 y 8000 caracteres.',
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
    
    document.getElementById("enviarG").addEventListener("click", function(event) {
        handleFormSubmit(event, 'form2');
    });

    document.getElementById("enviarGYS").addEventListener("click", function(event) {
        window.location.href = `/seleccionar-entidad-aliada/${id_proyecto}/`;
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
        if (fieldExclude.includes(field.id)){
            var index = fieldExclude.indexOf(field.id);
            if (inputs[index].value == 'False'){   
                field.classList.remove("is-invalid");
                field.classList.add("is-valid");
                feedback.textContent = '';
                return true;
            }
        }
        if (document.getElementById('recursos_dinero_entidad_aliada').value == 0){
            field.classList.remove("is-invalid");
            field.classList.add("is-valid");
            feedback.textContent = '';
            key = false
            return true;
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
    fetch(`/proyecto/info-proyecto/centro-formacion/${id_proyecto}/`, {
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
            limpiarInputs()
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
    var recursos_especie_entidad = document.getElementById("recursos_especie_entidad").value;
    var descripcion_recursos_especie_aportados = document.getElementById("descripcion_recursos_especie_aportados").value;
    var recursos_dinero_entidad_aliada = document.getElementById("recursos_dinero_entidad_aliada").value;
    var descripcion_destinacion_dinero_aportado = document.getElementById("descripcion_destinacion_dinero_aportado").value;
    var nombre_grupo_inv_entidad_aliada = document.getElementById("nombre_grupo_inv_entidad_aliada").value;
    var codigo_gruplac_entidad_aliada = document.getElementById("codigo_gruplac_entidad_aliada").value;
    var link_gruplac_entidad_aliada = document.getElementById("link_gruplac_entidad_aliada").value;
    var actividades_desarrollar_entidad_aliada_marco_proyecto = document.getElementById("actividades_desarrollar_entidad_aliada_marco_proyecto").value;
    var metodologia_act_transferencia_centro_formacion = document.getElementById("metodologia_act_transferencia_centro_formacion").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const elementos = [];

    let i = 1;
    while (true) {
        const elemento = document.getElementById(`objEspecifico${i}`);
        if (elemento) {
            elementos.push(elemento.checked);
            console.log(`Elemento ${i}:`, elemento.checked);
        } else {
            break;
        }
        
        i++;
    }

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    if (document.getElementById('id_entidad').value == ''){
        
    }else{
        formData.append("id_entidad", document.getElementById('id_entidad').value);
    }
    formData.append("nombre_entidad",nombre_entidad);
    formData.append("tipo_entidad_aliada", tipo_entidad);
    formData.append("naturaleza_entidad", naturaleza_entidad);
    formData.append("clasificacion_empresa", clasificacion_empresa);
    formData.append("nit", nit);
    formData.append("convenio", convenio);
    formData.append("especifique_tipo_codigo_convenio", especifique_tipo_codigo_convenio);
    formData.append("recursos_especie_entidad", recursos_especie_entidad);
    formData.append("descripcion_recursos_especie_aportados", descripcion_recursos_especie_aportados);
    formData.append("recursos_dinero_entidad_aliada", recursos_dinero_entidad_aliada);
    formData.append("descripcion_destinacion_dinero_aportado", descripcion_destinacion_dinero_aportado);
    formData.append("nombre_grupo_inv_entidad_aliada", nombre_grupo_inv_entidad_aliada);
    formData.append("codigo_gruplac_entidad_aliada", codigo_gruplac_entidad_aliada);
    formData.append("link_gruplac_entidad_aliada", link_gruplac_entidad_aliada);
    formData.append("actividades_desarrollar_entidad_aliada_marco_proyecto", actividades_desarrollar_entidad_aliada_marco_proyecto);
    formData.append("objetivo_especificos_relacionados", JSON.stringify(elementos));
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
                
                actualizarTabla(data.entidades);

                const input = document.getElementById('id_entidad');
                input.value = '';
            }
        })
    .catch(error => {
        console.error('Error en la solicitud:', error);
    });
};


function actualizarTabla(entidades) {
    // Obtener el elemento de la tabla por su clase
    const tabla = document.querySelector('.tablita');
  
    // Si la tabla existe, eliminarla
    if (tabla) {
      tabla.remove();
    }
  
    // Crear una nueva tabla
    const nuevaTabla = document.createElement('table');
    nuevaTabla.classList.add('tablita', 'table');
  
    // Crear el encabezado de la tabla
    const thead = document.createElement('thead');
    const encabezado = `
      <tr>
          <th>Nombre entidad</th>
          <th>NIT</th>
          <th>Tipo entidad</th>
          <th>Naturaleza entidad</th>
          <th>Clasificación empresa</th>
          <th>Opciones</th>
      </tr>
    `;
    thead.innerHTML = encabezado;
    nuevaTabla.appendChild(thead);
  
    // Crear el cuerpo de la tabla
    const tbody = document.createElement('tbody');
    entidades.forEach(entidad => {
      const fila = `
        <tr>
            <td>${entidad.nombre_entidad}</td>
            <td>${entidad.nit}</td>
            <td>${entidad.tipo_entidad_aliada}</td>
            <td>${entidad.naturaleza_entidad}</td>
            <td>${entidad.clasificacion_empresa}</td>
            <td>
                <button onclick="edit_entidad(${entidad.id})" type="button" class="btn btn-success">Editar</button>
                <button onclick="eliminarEntidad(${entidad.id})" type="button" class="btn btn-danger">Eliminar</button>
            </td>
        </tr>
      `;
      tbody.innerHTML += fila;
    });
    nuevaTabla.appendChild(tbody);
  
    // Agregar la nueva tabla al documento
    const contenedorTabla = document.getElementById('tabla-container');
    contenedorTabla.appendChild(nuevaTabla);
  }