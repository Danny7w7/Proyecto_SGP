inputs = [
     "objetivo_especifico1",
     "objetivo_especifico2",
     "objetivo_especifico3",
];
function showdivObj() {
     inputs.forEach((input, i) => {
          if (!(document.getElementById(input).value == "")) {
               document.getElementById(`Actividad${i + 1}`).style.display =
                    "block";
               document.getElementById(`divSiguiente`).style.display = "block";
               document.getElementById(`text-sapo`).style.display = "none";
          }
     });
}

let conjuntosMostrados = 1;
function mostrarDivs() {
     // Mostrar conjuntos adicionales solo si no se han mostrado más de 2
     if (conjuntosMostrados < 2) {
          document.querySelector(".la_prueba2").style.display = "block";
          conjuntosMostrados++;
     } else if (conjuntosMostrados == 2) {
          document.querySelector(".la_prueba3").style.display = "block";
          conjuntosMostrados++;
     } else {
          // alert('Solo puedes crear 3 objetivos especificos por proyecto.')
          Swal.fire({
               title: "¡Advertencia!",
               text: "Solo puede crear 3 objetivos específicos por proyecto.",
               icon: "warning",
               confirmButtonText: "Aceptar",
          });
     }
}
document.addEventListener("DOMContentLoaded", function () {
     const button1 = document.getElementById("step2");

     const collapse1 = document.getElementById("collapseOne");
     const collapse2 = document.getElementById("collapseTwo");
     const allValidations = {
          //Estructura del proyecto
          "form1": {
               "objetivo_general": {
                    pattern: /^[\s\S]{5,500}$/,
                    errorMsg:
                         "El obj general no es válido. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales",
               },
               "objetivo_especifico1": {
                    pattern: /^[\s\S]{5,500}$/,
                    errorMsg:
                         "El obj especifico no es válido. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales",
               },
               "objetivo_especifico2": {
                    pattern: /^[\s\S]{5,500}$/,
                    errorMsg:
                         "El obj especifico 2 no es válido. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales",
               },
               "objetivo_especifico3": {
                    pattern: /^[\s\S]{5,500}$/,
                    errorMsg:
                         "El obj especifico 3 no es válido. Debe tener entre 5 y 500 caracteres y no puede contener caracteres especiales",
               },
          },
          "form2": {
               "actividad1": {
                    pattern: /^[\s\S]{5,1000}$/,
                    errorMsg:
                         "La actividad de obj especifico 1 no es válida. Debe tener entre 5 y 1000 caracteres y no puede contener caracteres especiales",
               },
               "actividad2": {
                    pattern: /^[\s\S]{5,1000}$/,
                    errorMsg:
                         "La actividad de obj especifico 2 no es válida. Debe tener entre 5 y 1000 caracteres y no puede contener caracteres especiales",
               },
               "actividad3": {
                    pattern: /^[\s\S]{5,1000}$/,
                    errorMsg:
                         "La actividad de obj especifico 3 no es válida. Debe tener entre 5 y 1000 caracteres y no puede contener caracteres especiales",
               },
               "causa1": {
                    pattern: /^[\s\S]{5,1000}$/,
                    errorMsg:
                         "La causa no es válida. Debe tener entre 5 y 1000 caracteres y no puede contener caracteres especiales",
               },
               "causa2": {
                    pattern: /^[\s\S]{5,1000}$/,
                    errorMsg:
                         "La causa 2 no es válida. Debe tener entre 5 y 1000 caracteres y no puede contener caracteres especiales",
               },
               "causa3": {
                    pattern: /^[\s\S]{5,1000}$/,
                    errorMsg:
                         "La causa 3 no es válida. Debe tener entre 5 y 1000 caracteres y no puede contener caracteres especiales",
               },
               "efecto1": {
                    pattern: /^[\s\S]{5,1000}$/,
                    errorMsg:
                         "El efecto 1 no es válido. Debe tener entre 5 y 1000 caracteres y no puede contener caracteres especiales",
               },
               "efecto2": {
                    pattern: /^[\s\S]{5,1000}$/,
                    errorMsg:
                         "El efecto 2 no es válido. Debe tener entre 5 y 1000 caracteres y no puede contener caracteres especiales",
               },
               "efecto3": {
                    pattern: /^[\s\S]{5,1000}$/,
                    errorMsg:
                         "El efecto 3 no es válido. Debe tener entre 5 y 1000 caracteres y no puede contener caracteres especiales",
               },
          },
     };

     // Verificador de caracteres
     function handleTextareaInput(textarea, counterId) {
          const counter = document.getElementById(counterId);
          const val_jus = parseInt(counter.nextElementSibling.value);

          function updateCounter() {
               const currentLength = textarea.value.length;
               counter.textContent = `${currentLength}/${val_jus} máximo`;
          }

          textarea.addEventListener("input", updateCounter);

          // Llama a updateCounter para actualizar el contador cuando se carga la información
          updateCounter();
     }

     const textarea1 = document.getElementById("objetivo_general");
     const textarea2 = document.getElementById("objetivo_especifico1");
     const textarea3 = document.getElementById("objetivo_especifico2");
     const textarea4 = document.getElementById("objetivo_especifico3");
     const textarea5 = document.getElementById("actividad1");
     const textarea6 = document.getElementById("causa1");
     const textarea7 = document.getElementById("efecto1");
     const textarea8 = document.getElementById("actividad2");
     const textarea9 = document.getElementById("causa2");
     const textarea10 = document.getElementById("efecto2");
     const textarea11 = document.getElementById("actividad3");
     const textarea12 = document.getElementById("causa3");
     const textarea13 = document.getElementById("efecto3");

     handleTextareaInput(textarea1, "char-counter1");
     handleTextareaInput(textarea2, "char-counter2");
     handleTextareaInput(textarea3, "char-counter3");
     handleTextareaInput(textarea4, "char-counter4");
     handleTextareaInput(textarea5, "char-counter5");
     handleTextareaInput(textarea6, "char-counter6");
     handleTextareaInput(textarea7, "char-counter7");
     handleTextareaInput(textarea8, "char-counter8");
     handleTextareaInput(textarea9, "char-counter9");
     handleTextareaInput(textarea10, "char-counter10");
     handleTextareaInput(textarea11, "char-counter11");
     handleTextareaInput(textarea12, "char-counter12");
     handleTextareaInput(textarea13, "char-counter13");

     // Itera sobre cada conjunto de validaciones
     for (let formKey in allValidations) {
          for (let fieldId in allValidations[formKey]) {
               const inputField = document.getElementById(fieldId);

               // Verifica si el inputField realmente existe
               if (!inputField) {
                    console.error(
                         `El campo con id ${fieldId} no fue encontrado.`
                    );
                    continue;
               }

               const feedbackElement = inputField.nextElementSibling;
               const { pattern, errorMsg } = allValidations[formKey][fieldId];

               inputField.addEventListener("input", function () {
                    let senduwu = false;
                    validateField(
                         inputField,
                         feedbackElement,
                         pattern,
                         errorMsg
                    );
               });
          }
     }

     //ids de los formularios
     const form1 = document.getElementById("form1");

     document.getElementById("enviar1").addEventListener("click", function () {
          handleFormSubmit(event, "form1");
     });
     document.getElementById("enviar2").addEventListener("click", function () {
          handleFormSubmit(event, "form2");
     });

     function handleFormSubmit(event, formKey) {
          let isValid = true;

          for (let fieldId in allValidations[formKey]) {
               const inputField = document.getElementById(fieldId);

               // Nueva comprobación para evitar errores
               if (!inputField) continue;

               const feedbackElement = inputField.nextElementSibling;
               const { pattern, errorMsg } = allValidations[formKey][fieldId];

               isValid =
                    validateField(
                         inputField,
                         feedbackElement,
                         pattern,
                         errorMsg
                    ) && isValid;
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
                         button1.setAttribute(
                              "aria-expanded",
                              button1.getAttribute("aria-expanded") === "true"
                                   ? "false"
                                   : "true"
                         );
                         progress.setAttribute(
                              "value",
                              (1 * 100) / (stepButtons.length - 1)
                         );
                         collapse1.classList.remove("show");
                         collapse2.classList.add("show");
                    } else if (formKey == "form2") {
                         sendPost2();
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

function sendPost1() {
     var id_proyecto = document.getElementById("id_proyecto").value;
     // Crear un objeto FormData para los datos del formulario
     var formData = new FormData();
     formData.append(
          "objetivo_general",
          document.getElementById("objetivo_general").value
     );
     if (!(document.getElementById("objetivo_especifico1").value == "")) {
          formData.append(
               "objetivo_especifico1",
               document.getElementById("objetivo_especifico1").value
          );
     }
     if (!(document.getElementById("objetivo_especifico2").value == "")) {
          formData.append(
               "objetivo_especifico2",
               document.getElementById("objetivo_especifico2").value
          );
     }
     if (!(document.getElementById("objetivo_especifico3").value == "")) {
          formData.append(
               "objetivo_especifico3",
               document.getElementById("objetivo_especifico3").value
          );
     }
     formData.append(
          "csrfmiddlewaretoken",
          document.querySelector("[name=csrfmiddlewaretoken]").value
     );
     // Realizar una solicitud POST utilizando Fetch
     fetch(`/proyecto/arbol-problemas/objetivos/${id_proyecto}/`, {
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
                    showdivObj();
               }
          });
}

function sendPost2() {
     var id_proyecto = document.getElementById("id_proyecto").value;
     // Crear un objeto FormData para los datos del formulario
     var formData = new FormData();
     if (!(document.getElementById("actividad1").value == "")) {
          formData.append(
               "actividad1",
               document.getElementById("actividad1").value
          );
          formData.append("causa1", document.getElementById("causa1").value);
          formData.append("efecto1", document.getElementById("efecto1").value);
     }
     if (!(document.getElementById("actividad2").value == "")) {
          formData.append(
               "actividad2",
               document.getElementById("actividad2").value
          );
          formData.append("causa2", document.getElementById("causa2").value);
          formData.append("efecto2", document.getElementById("efecto2").value);
     }
     if (!(document.getElementById("actividad3").value == "")) {
          formData.append(
               "actividad3",
               document.getElementById("actividad3").value
          );
          formData.append("causa3", document.getElementById("causa3").value);
          formData.append("efecto3", document.getElementById("efecto3").value);
     }
     formData.append(
          "csrfmiddlewaretoken",
          document.querySelector("[name=csrfmiddlewaretoken]").value
     );
     // Realizar una solicitud POST utilizando Fetch
     fetch(`/proyecto/arbol-problemas/actividades/${id_proyecto}/`, {
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
                    window.location.href = `/seleccionar-objetivo/${id_proyecto}/`;
               }
          });
}
