document.addEventListener("DOMContentLoaded", function() {
    
    const allValidations = {
        //Validacion info proponente
       "form1": {
        "Nombre_Director": {
            pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,50}$/u,
            errorMsg: 'El nombre no es válido. Debe tener entre 5 y 50 caracteres y solo puede contener letras y espacios'
        },
        "email_director": {
            pattern: /^[a-zA-Z0-9._%+-ñÑ,]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
            errorMsg: 'El correo no es válido. Debe tener entre 5 y 100 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        },
        "Numero_Director": {
            pattern: /^\d{10}$/,
            errorMsg: 'El número no es válido. Debe tener 10 digitos númericos',
        },
        "Nombre_Sub_Director": {
            pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,50}$/u,
            errorMsg: 'El nombre no es válido. Debe tener entre 5 y 50 caracteres y solo puede contener letras y espacios'
        },
        "email_sub_director": {
            pattern: /^[a-zA-Z0-9._%+-ñÑ,]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
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
            pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,50}$/u,
            errorMsg: 'El nombre no es válido. Debe tener entre 5 y 50 caracteres y solo puede contener letras y espacios'
        },
        "Numero_Cedula_Autor": {
            pattern: /^\d{5,20}$/,
            errorMsg: 'El número de documento no es válido. Debe tener digitos númericos',
        },
        "Email_Autor_Proyecto": {
            pattern: /^[a-zA-Z0-9._%+-ñÑ,]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
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
            pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{5,50}$/u,
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
            pattern: /^[a-zA-Z0-9._%+-ñÑ,]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
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
        "link_video_proyecto": {
            pattern: /^(http|https):\/\/[^ "]+$/,
            errorMsg: 'El link no es válido.',
        },
        "justificacion_Economia_Naranja":{
            pattern: /^[A-Za-záéíóúÁÉÍÓÚñÑ, .]{5,500}$/,
            errorMsg: 'La justificación no es válida. Debe tener entre 5 y 500 caracteres y solo puede contener letras y espacios',
        }, 
        "justificacion_Politica_Discapacidad":{
            pattern: /^[A-Za-záéíóúÁÉÍÓÚñÑ, .]{5,500}$/,
            errorMsg: 'La justificación no es válida. Debe tener entre 5 y 500 caracteres y solo puede contener letras y espacios',
        }, 
        "justificacion_Industrial":{
            pattern: /^[A-Za-záéíóúÁÉÍÓÚñÑ, .]{5,500}$/,
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


    document.getElementById("enviar1").addEventListener("click", function(event) {
        handleFormSubmit(event, 'form1');
    });

    document.getElementById("enviar2").addEventListener("click", function(event) {
        handleFormSubmit(event, 'form2');
    });

    document.getElementById("enviar3").addEventListener("click", function(event) {
        handleFormSubmit(event, 'form3');
    });

    document.getElementById("enviar4").addEventListener("click", function(event) {
        handleFormSubmit(event, 'form4');
    });

    function handleFormSubmit(event, formKey) {
        let isValid = true;
        
                        // Verifica cuántas filas hay en la tabla (autores registrados)
                var numRows = document.querySelectorAll('.table tbody tr').length;

                // Si ya hay 3 autores, muestra una alerta y no envía la solicitud POST
                if (formKey === 'form2' && numRows > 3) {
                    Swal.fire({
                        title: 'Advertencia',
                        text: 'Ya has alcanzado el límite de 3 autores para este proyecto.',
                        icon: 'warning',
                        confirmButtonText: 'Aceptar'
                    });
                    event.preventDefault(); // Detener el envío del formulario
                    return;
                }

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
                }else if (formKey == 'form2'){
                    sendPost2()
                }
                else if (formKey == 'form3'){
                    sendPost3()
                }
                else if (formKey == 'form4'){
                    sendPost4()
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
    // Obtener los valores de los campos del formulario
    var region = document.getElementById("select_box").value; 
    var regional = document.getElementById("select_box2").value;
    var nombre_centro_formacion = document.getElementById("select_box3").value;
    var nombre_Director = document.getElementById("Nombre_Director").value;
    var email_director = document.getElementById("email_director").value;
    var numero_Director = document.getElementById("Numero_Director").value;
    var nombre_Sub_Director = document.getElementById("Nombre_Sub_Director").value;
    var email_sub_director = document.getElementById("email_sub_director").value;
    var numero_Sub_Director = document.getElementById("Numero_Sub_Director").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("Region", region);
    formData.append("Regional", regional);
    formData.append("Nombre_centro_formacion", nombre_centro_formacion);
    formData.append("Nombre_Director", nombre_Director);
    formData.append("Numero_Director", numero_Director);
    formData.append("email_director", email_director);
    formData.append("Nombre_Sub_Director", nombre_Sub_Director);
    formData.append("email_sub_director", email_sub_director);
    formData.append("Numero_Sub_Director", numero_Sub_Director);
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/info-proyecto/info-proponente/${id_proyecto}/`, {
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

// Autores
function sendPost2() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    console.log(id_proyecto)

        // // Verifica cuántas filas hay en la tabla (autores registrados)
        // var numRows = document.querySelectorAll('.table tbody tr').length;

        // // Si ya hay 3 autores, muestra una alerta y no envía la solicitud POST
        // if (numRows >= 3) {
        //     Swal.fire({
        //         title: 'Advertencia',
        //         text: 'Ya has alcanzado el límite de 3 autores para este proyecto.',
        //         icon: 'warning',
        //         confirmButtonText: 'Aceptar'
        //     });
        //     return;
        // }

    // Obtener los valores de los campos del formulario
    var nombre_autor_proyecto = document.getElementById("Nombre_Autor_Proyecto").value;
    var tipo_vinculacion_entidad = document.getElementById("select_box4").value;
    var numero_cedula_autor = document.getElementById("Numero_Cedula_Autor").value;
    var rol_sennova_participantes_proyecto = document.getElementById("select_box5").value;
    var email_autor_proyecto = document.getElementById("Email_Autor_Proyecto").value;
    var numero_meses_vinculacion_autor = document.getElementById("Numero_meses_vinculacion_Autor").value;
    var numero_telefono_autor = document.getElementById("Numero_Telefono_Autor").value;
    var numero_horas_semanales_dedicadas_Autores = document.getElementById("Numero_horas_Semanales_dedicadas_Autores").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("nombre_Autor_Proyecto", nombre_autor_proyecto);
    formData.append("tipo_Vinculacion_entidad", tipo_vinculacion_entidad);
    formData.append("numero_Cedula_Autor", numero_cedula_autor);
    formData.append("rol_Sennova_De_Participantes_de_Proyecto", rol_sennova_participantes_proyecto);
    formData.append("email_Autor_Proyecto", email_autor_proyecto);
    formData.append("numero_meses_vinculacion_Autor", numero_meses_vinculacion_autor);
    formData.append("numero_Telefono_Autor", numero_telefono_autor);
    formData.append("numero_horas_Semanales_dedicadas_Autores", numero_horas_semanales_dedicadas_Autores);
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/info-proyecto/info-autor/${id_proyecto}/`, {
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
            let tableBody = document.querySelector('.table tbody');
            let newRow = tableBody.insertRow();
            
            newRow.insertCell(0).textContent = data.nuevo_autor.nombre_Autor_Proyecto;
            newRow.insertCell(1).textContent = data.nuevo_autor.tipo_Vinculacion_entidad;
            newRow.insertCell(2).textContent = data.nuevo_autor.numero_Cedula_Autor;
            newRow.insertCell(3).textContent = data.nuevo_autor.rol_Sennova_De_Participantes_de_Proyecto;
            newRow.insertCell(4).textContent = data.nuevo_autor.email_Autor_Proyecto;
            newRow.insertCell(5).textContent = data.nuevo_autor.numero_Telefono_Autor;
    
            let actionsCell = newRow.insertCell(6);
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

// Participantes
function sendPost3() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    console.log(id_proyecto)
    // Obtener los valores de los campos del formulario
    var nombre_participantes_de_desarrollo = document.getElementById("Nombre_participantes_de_desarrollo").value;
    var rol_sennova_de_participantes_de_proyecto = document.getElementById("select_box6").value;
    var numero_Cedula_participantes = document.getElementById("Numero_cedula_participantes").value;
    var numero_meses_vinculacion_participantes = document.getElementById("Numero_meses_vinculacion_participantes").value;
    var email_participantes_de_desarrollo = document.getElementById("Email_participantes_de_desarrollo").value;
    var numero_horas_semanales_dedicadas_participantes = document.getElementById("Numero_horas_Semanales_dedicadas_participantes").value;
    var numero_telefono_participantes = document.getElementById("Numero_Telefono_participantes").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("nombre_participantes_de_desarrollo", nombre_participantes_de_desarrollo);
    formData.append("rol_Sennova_De_Participantes_de_Proyecto", rol_sennova_de_participantes_de_proyecto);
    formData.append("numero_cedula_participantes", numero_Cedula_participantes);
    formData.append("numero_meses_vinculacion_participantes", numero_meses_vinculacion_participantes);
    formData.append("email_participantes_de_desarrollo", email_participantes_de_desarrollo);
    formData.append("numero_horas_Semanales_dedicadas_participantes", numero_horas_semanales_dedicadas_participantes);
    formData.append("numero_Telefono_participantes", numero_telefono_participantes);
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/info-proyecto/info-participante/${id_proyecto}/`, {
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
            let tableBody = document.querySelector('.mitabla tbody');
            let newRow = tableBody.insertRow();
            
            newRow.insertCell(0).textContent = data.nuevo_participante.nombre_participantes_de_desarrollo;
            newRow.insertCell(1).textContent = data.nuevo_participante.numero_cedula_participantes;
            newRow.insertCell(2).textContent = data.nuevo_participante.numero_meses_vinculacion_participantes;
            newRow.insertCell(3).textContent = data.nuevo_participante.email_participantes_de_desarrollo;
            newRow.insertCell(4).textContent = data.nuevo_participante.numero_horas_Semanales_dedicadas_participantes;
            newRow.insertCell(5).textContent = data.nuevo_participante.numero_Telefono_participantes;
    
            let actionsCell = newRow.insertCell(6);
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

// Generalidades
function sendPost4() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    // Obtener los valores de los campos del formulario
    var codigo_dependencia_presupuestal = document.getElementById("select_box7").value;
    var tematicas_estrategias_sena = document.getElementById("select_box8").value;
    var link_video_proyecto = document.getElementById("link_video_proyecto").value;
    var proyecto_relacionado_industrial40 = document.getElementById("proyecto_Relacionado_Industrial40").value;
    var justificacion_industrial = document.getElementById("justificacion_Industrial").value;
    var actividades_economicas_del_proyecto_investigacion = document.getElementById("select_box9").value;
    var proyecto_relacionado_economia_naranja = document.getElementById("proyecto_Relacionado_Economia_Naranja").value;
    var justificacion_economia_naranja = document.getElementById("justificacion_Economia_Naranja").value;
    var proyecto_relacionado_politica_discapacidad = document.getElementById("proyecto_Relacionado_Politica_Discapacidad").value;
    var justificacion_politica_discapacidad = document.getElementById("justificacion_Politica_Discapacidad").value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(csrfToken)

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append("codigo_Dependencia_Presupuestal", codigo_dependencia_presupuestal);
    formData.append("tematicas_Estrategias_SENA", tematicas_estrategias_sena);
    formData.append("link_video_proyecto", link_video_proyecto);
    formData.append("proyecto_Relacionado_Industrial40", proyecto_relacionado_industrial40);
    formData.append("justificacion_Industrial", justificacion_industrial);
    formData.append("actividades_economicas_del_proyecto_investigacion", actividades_economicas_del_proyecto_investigacion);
    formData.append("proyecto_Relacionado_Economia_Naranja", proyecto_relacionado_economia_naranja);
    formData.append("justificacion_Economia_Naranja", justificacion_economia_naranja);
    formData.append("proyecto_Relacionado_Politica_Discapacidad", proyecto_relacionado_politica_discapacidad);
    formData.append("justificacion_Politica_Discapacidad", justificacion_politica_discapacidad);
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/info-proyecto/info-generalidades/${id_proyecto}/`, {
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