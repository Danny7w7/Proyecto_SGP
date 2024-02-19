var id_proyecto = document.getElementById("id_proyecto").value;
function edit_autor(id) {
    const selectDiv = document.getElementById(`autor${id}`);
    const inputs = selectDiv.querySelectorAll('input[type="hidden"]');

    for (let i = 0; i < inputs.length; i++) {
        let texto = inputs[i].id;
        texto = texto.substring(0, texto.length - 7);
        const changeDiv = document.getElementById(texto);
        changeDiv.value = inputs[i].value;
    }
}
function edit_participantes(id) {
    const selectDiv = document.getElementById(`participante${id}`);
    const inputs = selectDiv.querySelectorAll('input[type="hidden"]');

    for (let i = 0; i < inputs.length; i++) {
        let texto = inputs[i].id;
        texto = texto.substring(0, texto.length - 7);
        const changeDiv = document.getElementById(texto);
        changeDiv.value = inputs[i].value;
    }
}


document.addEventListener("DOMContentLoaded", function () {
    getRegiones()

    var fieldQuestion = [];
    var fieldExclude = [];
    const textsArea = []
    
    //Obtengo todos los inputs de preguntas politicas agregador por el contex de Django
    fieldQuestionAddByDjango = document.getElementsByClassName('fieldQuestionAddByDjango')
    fieldExcludeAddByDjango = document.getElementsByClassName('fieldExcludeAddByDjango')
    for (let i = 0; i < fieldQuestionAddByDjango.length; i++) {
        fieldQuestion.push(fieldQuestionAddByDjango[i].id)
        fieldExclude.push(fieldExcludeAddByDjango[i].id)
        textsArea.push(fieldExcludeAddByDjango[i])
    }

    for (let i = 0; i < fieldQuestionAddByDjango.length; i++) {
        fieldQuestionAddByDjango[i].addEventListener("change", function () {
            if (fieldQuestionAddByDjango[i].value == 0) {
                fieldExcludeAddByDjango[i].readOnly = true;
            }else{
                fieldExcludeAddByDjango[i].readOnly = false;
            }
        });
    }

    var inputs = fieldQuestion.map(function (id) {
        return document.getElementById(id);
    });

    // Verificador de caracteres
    function handleTextareaInput(textarea, counterId) {
        let counter = null;
        while (counterId<1000) {
            // Intento obtener el elemento con el ID char-counter
            counter = document.getElementById(`char-counter${counterId}`);
            // Compruebo si este existe para asi salir del ciclo while
            if (counter){
                counterId = 1000
            }
            // En caso de que no exista se va a aumentar el ID del counter para que intente obtener el siguiente y asi continuar con el ciclo hasta que lo obtenga
            counterId++;
        }
        const val_jus = parseInt(counter.nextElementSibling.value);

        function updateCounter() {
            const currentLength = textarea.value.length;
            counter.textContent = `${currentLength}/${val_jus} máximo`;
        }

        textarea.addEventListener("input", updateCounter);

        // Llama a updateCounter para actualizar el contador cuando se carga la información
        updateCounter();
    }

    for (let i = 0; i < textsArea.length; i++) {
        handleTextareaInput(textsArea[i], i+1);
    }
    
    const buttons = [
        document.getElementById("step2"),
        document.getElementById("step3"),
        document.getElementById("step4"),
    ];

    const collapses = [
        document.getElementById("collapseOne"),
        document.getElementById("collapseTwo"),
        document.getElementById("collapseThree"),
        document.getElementById("collapseFour"),
    ];

    const allValidations = {
        //Validacion info proponente
       "form1": {
        "Nombre_Director": {
            pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s]{5,40}$/u,
            errorMsg: 'El nombre del director no es válido. Debe tener entre 5 y 40 caracteres y solo puede contener letras y espacios.'
        },
        "email_director": {
            pattern: /^[a-zA-Z0-9._%+-ñÑ,]+@sena[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
            errorMsg: 'El correo no es válido. Debe tener entre 5 y 40 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        },
        "Numero_Director": {
            pattern: /^.{5,30}$/,
            errorMsg: 'El número del director(a) no es válido. Debe tener una longitud entre 5 y 30 caracteres.',
        },
        "Nombre_Sub_Director": {
            pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s]{5,40}$/u,
            errorMsg: 'El nombre del subdirector(a) no es válido. Debe tener entre 5 y 40 caracteres y solo puede contener letras y espacios.'
        },
        "email_sub_director": {
            pattern: /^[a-zA-Z0-9._%+-ñÑ,]+@sena[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
            errorMsg: 'El correo del subdirector(a) no es válido. Debe ser institucional sena.'
        },
        "Numero_Sub_Director": {
            pattern: /^.{5,30}$/,
            errorMsg: 'El número del subdirector(a) no es válido. Debe tener una longitud entre 5 y 30 caracteres.',
        },
       },
       // Validacion autor
       "form2":{
        "Nombre_Autor_Proyecto": {
            pattern: /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s]{5,40}$/u,
            errorMsg: 'El nombre no es válido. Debe tener entre 5 y 40 caracteres y solo puede contener letras y espacios.'
        },
        "Numero_Cedula_Autor": {
            pattern: /^\d{5,20}$/,
            errorMsg: 'El número de documento no es válido. Debe tener digitos númericos.',
        },
        "Email_Autor_Proyecto": {
            pattern: /^[a-zA-Z0-9._%+-ñÑ,]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
            errorMsg: 'El correo no es válido. Debe tener entre 5 y 40 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        },
        "Numero_meses_vinculacion_Autor": {
            pattern: /^(?:[1-9]|1[0-1]|1?\.\d|[1-9]\.\d|10\.\d|11\.[0-9]|12)$/i,
            errorMsg: 'El número de meses de vinculación no es válido. Debe ser un número entre 1 y 12, opcionalmente seguido de un único dígito después del punto decimal.'
        },
        "Numero_Telefono_Autor": {
            pattern: /^.{5,30}$/,
            errorMsg: 'El número no es válido. Debe tener una longitud entre 5 y 30 caracteres.',
        },
        "Numero_horas_Semanales_dedicadas_Autores": {
            pattern: /^(?:[0-9]|[1-3][0-9]|4[0-8])$/,
            errorMsg: 'El número de horas no es válido. Debe tener digitos númericos y máximo 48 horas.',
        },
       },
        //Validacion participantes
       "form3":{
        "Nombre_participantes_de_desarrollo":{
            pattern:  /^[a-zA-ZÀ-ÿ\u00f1\u00d1\d ,.\s]{5,40}$/u,
            errorMsg: 'El nombre de participantes no es válido. Debe tener entre 5 y 40 caracteres y solo puede contener letras y espacios',
        }, 
        "Numero_cedula_participantes": {
            pattern: /^\d{5,20}$/,
            errorMsg: 'El número de documento no es válido. Debe tener digitos númericos',
        },
        "Numero_meses_vinculacion_participantes": {
            pattern: /^(?:[1-9]|1[0-1]|1?\.\d|[1-9]\.\d|10\.\d|11\.[0-9]|12)$/i,
            errorMsg: 'El número de meses de vinculación no es válido. Debe ser un número entre 1 y 12, opcionalmente seguido de un único dígito después del punto decimal.'
        },
        "Email_participantes_de_desarrollo": {
            pattern: /^[a-zA-Z0-9._%+-ñÑ,]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
            errorMsg: 'El correo de participantes no es válido. Debe tener entre 5 y 40 caracteres y solo puede contener letras, números, espacios, puntos y comas.'
        },
        "Numero_horas_Semanales_dedicadas_participantes": {
            pattern: /^(?:[0-9]|[1-3][0-9]|4[0-8])$/,
            errorMsg: 'El número de horas no es válido. Debe tener digitos númericos y máximo 48 horas.',
        },
        "Numero_Telefono_participantes": {
            pattern: /^\d{10}$/,
            errorMsg: 'El número de teléfono no es válido. Debe tener 10 digitos númericos.',
        },
       },
       "form4":{
        "link_video_proyecto": {
            pattern: /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/,
            errorMsg: 'El link del vídeo no es válido.',
        },
       }
    };

    for (let i = 0; i < fieldExclude.length; i++) {
        allValidations.form4[fieldExclude[i]] = {
            pattern: /^[\s\S]{5,600}$/,
            errorMsg: 'La justificación no es válida. Debe tener entre 5 y 600 caracteres y solo puede contener letras y espacios.',
        };
    }

    // Itera sobre cada conjunto de validaciones
    for (let formKey in allValidations) {
        for (let fieldId in allValidations[formKey]) {
            const inputField = document.getElementById(fieldId);

            // Verifica si el inputField realmente existe
            if (!inputField) {
                console.error(`El campo con id ${fieldId} no fue encontrado.`);
                continue;
            }

            const feedbackElement = inputField.nextElementSibling;
            const { pattern, errorMsg } = allValidations[formKey][fieldId];

            inputField.addEventListener("input", function () {
                validateField(inputField, feedbackElement, pattern, errorMsg);
            });
        }
    }

    //ids de los formularios
    const form1 = document.getElementById("form1");
    const form2 = document.getElementById("form2");

    document
        .getElementById("enviar1")
        .addEventListener("click", function (event) {
            handleFormSubmit(event, "form1");
            nextStep(0);
        });

    document
        .getElementById("enviarGAutores")
        .addEventListener("click", function (event) {
            handleFormSubmit(event, "form2");
        });

    document
        .getElementById("sigAutores")
        .addEventListener("click", function (event) {
            nextStep(1);
        });

    document
        .getElementById("enviarGParticipantes")
        .addEventListener("click", function (event) {
            handleFormSubmit(event, "form3");
        });

    document
        .getElementById("enviarGYSParticipantes")
        .addEventListener("click", function (event) {
            nextStep(2);
        });

    document
        .getElementById("enviar4")
        .addEventListener("click", function (event) {
            handleFormSubmit(event, "form4");
        });

    function nextStep(i) {
        const currentButton = buttons[i];
        const currentcollapse = collapses[i];
        currentButton.setAttribute(
            "aria-expanded",
            currentButton.getAttribute("aria-expanded") === "true"
                ? "false"
                : "true"
        );
        progress.setAttribute(
            "value",
            ((i + 1) * 100) / (stepButtons.length - 1)
        );
        collapses[i].classList.remove("show");
        collapses[i + 1].classList.add("show");
    }

    function handleFormSubmit(event, formKey) {
        let isValid = true;
        // Verifica cuántas filas hay en la tabla (autores registrados)
        var numRows = document.querySelectorAll(
            "#table_autores tbody tr"
        ).length;

        // Si ya hay 3 autores, muestra una alerta y no envía la solicitud POST
        if (formKey === "form2" && numRows > 2) {
            Swal.fire({
                title: "Advertencia",
                text: "Ya has alcanzado el límite de 3 autores para este proyecto.",
                icon: "warning",
                confirmButtonText: "Aceptar",
            });
            event.preventDefault(); // Detener el envío del formulario
            return;
        }

        for (let fieldId in allValidations[formKey]) {
            const inputField = document.getElementById(fieldId);

            // Nueva comprobación para evitar errores
            if (!inputField) continue;

            const feedbackElement = inputField.nextElementSibling;
            const { pattern, errorMsg } = allValidations[formKey][fieldId];

            isValid =
                validateField(inputField, feedbackElement, pattern, errorMsg) &&
                isValid;
        }
        event.preventDefault();
        if (isValid) {
            Swal.fire({
                title: "¡Éxito!",
                text: "Información registrada correctamente.",
                icon: "success",
                confirmButtonText: "Aceptar",
            }).then(() => {
                if (formKey == "form1") {
                    sendPost1();
                } else if (formKey == "form2") {
                    sendPost2();
                    clearinputs(formKey);
                } else if (formKey == "form3") {
                    sendPost3();
                    clearinputs(formKey);
                } else if (formKey == "form4") {
                    sendPost4();
                }
            });
        } else {
            Swal.fire({
                title: "Error!",
                text: "Por favor, corrija los errores en el formulario antes de enviar.",
                icon: "error",
                confirmButtonText: "Aceptar",
            });
        }
    }

    function validateField(field, feedback, pattern, errorMsg) {
        if (fieldExclude.includes(field.id)) {
            var index = fieldExclude.indexOf(field.id);
            if (inputs[index].value == "0") {
                field.classList.remove("is-invalid");
                field.classList.add("is-valid");
                feedback.textContent = "";
                return true;
            }
        }
        if (pattern.test(field.value)) {
            field.classList.remove("is-invalid");
            field.classList.add("is-valid");
            feedback.textContent = "";
            return true;
        } else {
            field.classList.remove("is-valid");
            field.classList.add("is-invalid");
            feedback.textContent = errorMsg;
            return false;
        }
    }
});

function clearinputs(form) {
    form = document.getElementById(form);
    const inputs = form.querySelectorAll("input");
    const selects = form.querySelectorAll("select");

    inputs.forEach((input) => {
        input.value = "";
    });
    selects.forEach((select) => {
        select.selectedIndex = 0;
    });
}

function sendPost1() {
    // Obtener los valores de los campos del formulario
    var region = document.getElementById("select_box").value;
    var regional = document.getElementById("select_box2").value;
    var nombre_centro_formacion = document.getElementById("select_box3").value;
    var nombre_Director = document.getElementById("Nombre_Director").value;
    var email_director = document.getElementById("email_director").value;
    var numero_Director = document.getElementById("Numero_Director").value;
    var nombre_Sub_Director = document.getElementById(
        "Nombre_Sub_Director"
    ).value;
    var email_sub_director =
        document.getElementById("email_sub_director").value;
    var numero_Sub_Director = document.getElementById(
        "Numero_Sub_Director"
    ).value;
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

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
        method: "POST",
        body: formData,
    })
        .then((response) => response.json()) // Parsea la respuesta JSON
        .then((data) => {
            if (data.error) {
                console.error("Error:", data.error);
                // Manejar el error, por ejemplo, mostrar un mensaje de error al usuario
            } else {
                console.log("Mensaje de éxito:", data.mensaje);
                // Realizar acciones de éxito, si es necesario
            }
        })
        .catch((error) => {
            console.error("Error en la solicitud:", error);
            // Manejar errores en la solicitud, como problemas de red
        });
}

// Autores
function sendPost2() {
    var id_proyecto = document.getElementById("id_proyecto").value;

    // Obtener los valores de los campos del formulario
    var nombre_autor_proyecto = document.getElementById(
        "Nombre_Autor_Proyecto"
    ).value;
    var tipo_vinculacion_entidad = document.getElementById(
        "tipo_Vinculacion_entidad"
    ).value;
    var numero_cedula_autor = document.getElementById(
        "Numero_Cedula_Autor"
    ).value;
    var rol_sennova_participantes_proyecto = document.getElementById(
        "rol_Sennova_De_Participantes_de_Proyecto"
    ).value;
    var email_autor_proyecto = document.getElementById(
        "Email_Autor_Proyecto"
    ).value;
    var numero_meses_vinculacion_autor = document.getElementById(
        "Numero_meses_vinculacion_Autor"
    ).value;
    var numero_telefono_autor = document.getElementById(
        "Numero_Telefono_Autor"
    ).value;
    var numero_horas_semanales_dedicadas_Autores = document.getElementById(
        "Numero_horas_Semanales_dedicadas_Autores"
    ).value;
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    if (document.getElementById("id_autor").value == "") {
       
    } else {
        formData.append("id_autor", document.getElementById("id_autor").value);
    }
    formData.append("nombre_Autor_Proyecto", nombre_autor_proyecto);
    formData.append("tipo_Vinculacion_entidad", tipo_vinculacion_entidad);
    formData.append("numero_Cedula_Autor", numero_cedula_autor);
    formData.append(
        "rol_Sennova_De_Participantes_de_Proyecto",
        rol_sennova_participantes_proyecto
    );
    formData.append("email_Autor_Proyecto", email_autor_proyecto);
    formData.append(
        "numero_meses_vinculacion_Autor",
        numero_meses_vinculacion_autor
    );
    formData.append("numero_Telefono_Autor", numero_telefono_autor);
    formData.append(
        "numero_horas_Semanales_dedicadas_Autores",
        numero_horas_semanales_dedicadas_Autores
    );
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/info-proyecto/info-autor/${id_proyecto}/`, {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json()) // Parsea la respuesta JSON
        .then((data) => {
            if (data.error) {
                console.error("Error:", data.error);
                alert(data.error); // O muestra el error de alguna otra manera
            } else {
                console.log("Mensaje de éxito:", data.mensaje);

                actualizarTablaAutores(data.autores);
                actualizarInputAutores(data.autores);

                const input = document.getElementById("id_autor");
                input.value = "";
            }
        })
        .catch((error) => {
            console.error("Error en la solicitud:", error);
            // Manejar errores en la solicitud, como problemas de red
        });
}

// Participantes
function sendPost3() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    console.log(id_proyecto);
    // Obtener los valores de los campos del formulario
    var nombre_participantes_de_desarrollo = document.getElementById(
        "Nombre_participantes_de_desarrollo"
    ).value;
    var rol_sennova_de_participantes_de_proyecto = document.getElementById(
        "Rol_Sennova_De_Participantes_de_Proyecto"
    ).value;
    var numero_Cedula_participantes = document.getElementById(
        "Numero_cedula_participantes"
    ).value;
    var numero_meses_vinculacion_participantes = document.getElementById(
        "Numero_meses_vinculacion_participantes"
    ).value;
    var email_participantes_de_desarrollo = document.getElementById(
        "Email_participantes_de_desarrollo"
    ).value;
    var numero_horas_semanales_dedicadas_participantes =
        document.getElementById(
            "Numero_horas_Semanales_dedicadas_participantes"
        ).value;
    var numero_telefono_participantes = document.getElementById(
        "Numero_Telefono_participantes"
    ).value;
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    if (document.getElementById("id_participante").value == "") {
        
    } else {
        formData.append(
            "id_participante",
            document.getElementById("id_participante").value
        );
    }
    formData.append(
        "nombre_participantes_de_desarrollo",
        nombre_participantes_de_desarrollo
    );
    formData.append(
        "rol_Sennova_De_Participantes_de_Proyecto",
        rol_sennova_de_participantes_de_proyecto
    );
    formData.append("numero_cedula_participantes", numero_Cedula_participantes);
    formData.append(
        "numero_meses_vinculacion_participantes",
        numero_meses_vinculacion_participantes
    );
    formData.append(
        "email_participantes_de_desarrollo",
        email_participantes_de_desarrollo
    );
    formData.append(
        "numero_horas_Semanales_dedicadas_participantes",
        numero_horas_semanales_dedicadas_participantes
    );
    formData.append(
        "numero_Telefono_participantes",
        numero_telefono_participantes
    );
    formData.append("csrfmiddlewaretoken", csrfToken);
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/info-proyecto/info-participante/${id_proyecto}/`, {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json()) // Parsea la respuesta JSON
        .then((data) => {
            if (data.error) {
                console.error("Error:", data.error);
                alert(data.error); // O muestra el error de alguna otra manera
            } else {
                console.log("Mensaje de éxito:", data.mensaje);

                actualizarTablaParticipantes(data.participantes);
                actualizarInputParticipantes(data.participantes);

                const input = document.getElementById("id_participante");
                input.value = "";
            }
        })
        .catch((error) => {
            console.error("Error en la solicitud:", error);
            // Manejar errores en la solicitud, como problemas de red
        });
}

// Generalidades
function sendPost4() {
    var id_proyecto = document.getElementById("id_proyecto").value;
    // Obtener los valores de los campos del formulario
    var codigo_dependencia_presupuestal =
    document.getElementById("select_box7").value;
    var tematicas_estrategias_sena =
    document.getElementById("select_box8").value;
    var link_video_proyecto = 
    document.getElementById("link_video_proyecto").value;
    var actividades_economicas_del_proyecto_investigacion =
    document.getElementById("select_box9").value;


    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Crear un objeto FormData para los datos del formulario
    var formData = new FormData();
    formData.append(
        "codigo_Dependencia_Presupuestal",
        codigo_dependencia_presupuestal
    );
    formData.append(
        "tematicas_Estrategias_SENA", 
        tematicas_estrategias_sena
    );
    formData.append(
        "link_video_proyecto", 
        link_video_proyecto
    );
    formData.append(
        "actividades_economicas_del_proyecto_investigacion", 
        actividades_economicas_del_proyecto_investigacion
    );


    for (let i = 0; i < fieldQuestionAddByDjango.length; i++) {
        if (fieldQuestionAddByDjango[i].value != 0) {
            formData.append(
                fieldQuestionAddByDjango[i].value,
                fieldExcludeAddByDjango[i].value
            )
        }
    }

    formData.append(
        "csrfmiddlewaretoken", 
        csrfToken
    );
    // Realizar una solicitud POST utilizando Fetch
    fetch(`/proyecto/info-proyecto/info-generalidades/${id_proyecto}/`, {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json()) // Parsea la respuesta JSON
        .then((data) => {
            if (data.error) {
                console.error("Error:", data.error);
                // Manejar el error, por ejemplo, mostrar un mensaje de error al usuario
            } else {
                console.log("Mensaje de éxito:", data.mensaje);
                window.location.href = `/estructura-proyecto/${id_proyecto}/`;
            }
        })
        .catch((error) => {
            console.error("Error en la solicitud:", error);
            // Manejar errores en la solicitud, como problemas de red
        });
}

function actualizarTablaAutores(autores) {
    // Obtener el elemento de la tabla por su clase
    const tabla = document.querySelector(".tabla_autores");

    // Si la tabla existe, eliminarla
    if (tabla) {
        tabla.remove();
    }

    // Crear una nueva tabla
    const nuevaTabla = document.createElement("table");
    nuevaTabla.classList.add("tablita", "table", "tabla_autores");

    // Crear el encabezado de la tabla
    const thead = document.createElement("thead");
    const encabezado = `
    <tr>
        <th>Nombre del autor(a)</th>
        <th>Tipo de vinculación</th>
        <th>Número de documento</th>
        <th>Rol sennova</th>
        <th>Correo electrónico</th>
        <th>Número de teléfono</th>
        <th>Acciones</th>
    </tr>
    `;
    thead.innerHTML = encabezado;
    nuevaTabla.appendChild(thead);

    // Crear el cuerpo de la tabla
    const tbody = document.createElement("tbody");
    autores.forEach((autor) => {
        const fila = `
        <tr>
            <td>${autor.nombre_Autor_Proyecto}</td>
            <td>${autor.tipo_Vinculacion_entidad}</td>
            <td>${autor.numero_Cedula_Autor}</td>
            <td>${autor.rol_Sennova_De_Participantes_de_Proyecto}</td>
            <td>${autor.email_Autor_Proyecto}</td>
            <td>${autor.numero_Telefono_Autor}</td>
            <td>
                <div class="btn-group" role="group" aria-label="Acciones">
                    <button onclick="edit_autor(${autor.id})" type="button" class="btn btn-success">Editar</button>
                </div>
            </td>
        </tr>
      `;
        tbody.innerHTML += fila;
    });
    nuevaTabla.appendChild(tbody);

    // Agregar la nueva tabla al documento
    const contenedorTabla = document.getElementById("tabla-container");
    contenedorTabla.appendChild(nuevaTabla);
}

function actualizarInputAutores(autores) {
    const selectDiv = document.getElementById("inputs_autores");

    if (selectDiv) {
        selectDiv.remove();
    }

    const contenedorInput = document.createElement("div");
    contenedorInput.id = "inputs_autores";

    autores.forEach((autor) => {
        const divAutor = document.createElement("div");
        divAutor.id = `autor${autor.id}`;

        divAutor.innerHTML = `
            <input id="id_autor_hidden" type="hidden" value="${autor.id}">
            <input id="Nombre_Autor_Proyecto_hidden" type="hidden" value="${autor.nombre_Autor_Proyecto}">
            <input id="tipo_Vinculacion_entidad_hidden" type="hidden" value="${autor.tipo_Vinculacion_entidad}">
            <input id="Numero_Cedula_Autor_hidden" type="hidden" value="${autor.numero_Cedula_Autor}">
            <input id="rol_Sennova_De_Participantes_de_Proyecto_hidden" type="hidden" value="${autor.rol_Sennova_De_Participantes_de_Proyecto}">
            <input id="Email_Autor_Proyecto_hidden" type="hidden" value="${autor.email_Autor_Proyecto}">
            <input id="Numero_meses_vinculacion_Autor_hidden" type="hidden" value="${autor.numero_meses_vinculacion_Autor}">
            <input id="Numero_Telefono_Autor_hidden" type="hidden" value="${autor.numero_Telefono_Autor}">
            <input id="Numero_horas_Semanales_dedicadas_Autores_hidden" type="hidden" value="${autor.numero_horas_Semanales_dedicadas_Autores}">
        `;

        contenedorInput.appendChild(divAutor);
    });

    const containerInputs = document.getElementById("container-inputs-autores");
    containerInputs.appendChild(contenedorInput);
}

function actualizarTablaParticipantes(participantes) {
    // Obtener el elemento de la tabla por su clase
    const tabla = document.querySelector(".tabla_participantes");

    // Si la tabla existe, eliminarla
    if (tabla) {
        tabla.remove();
    }

    // Crear una nueva tabla
    const nuevaTabla = document.createElement("table");
    nuevaTabla.classList.add("tablita", "table", "tabla_participantes");

    // Crear el encabezado de la tabla
    const thead = document.createElement("thead");
    const encabezado = `
<tr>
    <th>Nombres</th>
    <th>Número documento</th>
    <th>N° meses vinculación</th>
    <th>Email participantes</th>
    <th>N° horas semanales</th>
    <th>Telefono</th>
    <th>Acciones</th>
</tr>
`;
    thead.innerHTML = encabezado;
    nuevaTabla.appendChild(thead);

    // Crear el cuerpo de la tabla
    const tbody = document.createElement("tbody");
    participantes.forEach((participante) => {
        const fila = `
    <tr>
        <td>${participante.nombre_participantes_de_desarrollo}</td>
        <td>${participante.numero_cedula_participantes}</td>
        <td>${participante.numero_meses_vinculacion_participantes}</td>
        <td>${participante.email_participantes_de_desarrollo}</td>
        <td>${participante.numero_horas_Semanales_dedicadas_participantes}</td>
        <td>${participante.numero_Telefono_participantes}</td>
        <td>
            <div class="btn-group" role="group" aria-label="Acciones">
                <button onclick="edit_participantes(${participante.id})" type="button" class="btn btn-success">Editar</button>
            </div>
        </td>
    </tr>
    `;
        tbody.innerHTML += fila;
    });
    nuevaTabla.appendChild(tbody);

    // Agregar la nueva tabla al documento
    const contenedorTabla = document.getElementById("tabla-container-2");
    contenedorTabla.appendChild(nuevaTabla);
}

function actualizarInputParticipantes(participantes) {
    const selectDiv = document.getElementById("inputs_participantes");

    if (selectDiv) {
        selectDiv.remove();
    }

    const contenedorInput = document.createElement("div");
    contenedorInput.id = "inputs_participantes";

    participantes.forEach((participante) => {
        const divParticipante = document.createElement("div");
        divParticipante.id = `participante${participante.id}`;

        divParticipante.innerHTML = `
            <input id="id_participante_hidden" type="hidden" value="${participante.id}">
            <input id="Nombre_participantes_de_desarrollo_hidden" type="hidden" value="${participante.nombre_participantes_de_desarrollo}">
            <input id="Rol_Sennova_De_Participantes_de_Proyecto_hidden" type="hidden" value="${participante.rol_Sennova_De_Participantes_de_Proyecto}">
            <input id="Numero_cedula_participantes_hidden" type="hidden" value="${participante.numero_cedula_participantes}">
            <input id="Numero_meses_vinculacion_participantes_hidden" type="hidden" value="${participante.numero_meses_vinculacion_participantes}">
            <input id="Email_participantes_de_desarrollo_hidden" type="hidden" value="${participante.email_participantes_de_desarrollo}">
            <input id="Numero_horas_Semanales_dedicadas_participantes_hidden" type="hidden" value="${participante.numero_horas_Semanales_dedicadas_participantes}">
            <input id="Numero_Telefono_participantes_hidden" type="hidden" value="${participante.numero_Telefono_participantes}">
        `;

        contenedorInput.appendChild(divParticipante);
    });

    const containerInputs = document.getElementById(
        "container-inputs-participantes"
    );
    containerInputs.appendChild(contenedorInput);
}

function getRegiones() {
    fetch("/getRegiones/")
        .then((response) => {
            if (!response.ok) {
                throw new Error("La solicitud no fue exitosa");
            }
            return response.json();
        })
        .then((data) => {
            showRegional(data)
        })
        .catch((error) => {
            console.error("Error al realizar la solicitud:", error);
        });
};

function showRegional(data) {
    let id_region;
    let id_regional
    var selectRegion = document.getElementById("select_box");
    var selectRegional = document.getElementById("select_box2")
    
    selectRegion.addEventListener("change", function() {
        for (let i = 0; i < data.regiones.length; i++) {
            if (data.regiones[i].nombre == selectRegion.value){
                id_region = data.regiones[i].id
                break;
            }
        }
        const options = getArraybuttonOption("select_box2")
        for (let i = 0; i < data.regionales.length; i++) {
            if (data.regionales[i].region_id == id_region) {
                options[i+1].style.display = 'block';
            } else{
                options[i+1].style.display = 'none';
            }
        }
    });
    selectRegional.addEventListener("change", function() {
        for (let i = 0; i < data.regionales.length; i++) {
            if (data.regionales[i].nombre.toLowerCase() == selectRegional.value.toLowerCase()){
                id_regional = data.regionales[i].cod_regional
                break;
            }
        }
        const options2 = getArraybuttonOption("select_box3")
        for (let i = 0; i < data.centros.length; i++) {
            if (data.centros[i].region_id == id_regional) {
                options2[i+1].style.display = 'block';
            } else{
                options2[i+1].style.display = 'none';
            }
        }
    });
}

function getArraybuttonOption(id) {
    select = document.getElementById(id);
    button = select.nextElementSibling;
    elements = button.querySelector('.dselect-items');
    options = elements.getElementsByTagName('button');
    return options
}