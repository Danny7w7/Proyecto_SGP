
function validateFileType() {
    const fileInput = event.target;
    const allowedFileTypes = ['.docx', '.pdf'];

    if (fileInput.files.length > 0) {
        const selectedFile = fileInput.files[0];
        const fileExtension = '.' + selectedFile.name.split('.').pop();

        if (!allowedFileTypes.includes(fileExtension.toLowerCase())) {
            Swal.fire({
                title: 'Advertencia',
                text: 'Archivo no permitido. Por favor, selecciona un archivo .docx o .pdf',
                icon: 'warning',
                confirmButtonText: 'Aceptar'
            });
            fileInput.value = '';
        }
    }
}

function validarTamanioArchivo(input, maxSizeInBytes) {
    const files = input.files;

    for (let i = 0; i < files.length; i++) {
        if (files[i].size > maxSizeInBytes) {
            Swal.fire({
                title: 'Advertencia',
                text: 'El peso del archivo supera el límite',
                icon: 'warning',
                confirmButtonText: 'Aceptar'
            });
            input.value = '';
            return false;
        }
    }

    return true;
}

$(document).ready(function() {
    $('#form1').submit(function(event) {
        event.preventDefault();

        var formData = new FormData(this);
        var proyecto_id = $('#proyecto_id').val();

        // Agregar el proyecto_id al FormData
        formData.append('proyecto_id', proyecto_id);

        $.ajax({
            type: 'POST',
            url: '/subir_anexo/',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    Swal.fire({
                        title: '¡Éxito!',
                        text: 'Información registrada correctamente.',
                        icon: 'success',
                        confirmButtonText: 'Aceptar'
                    })
                } else {
                    alert('Error al subir los anexos: ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: "Completa todos los anexos antes de poder guardarlos"
                });
            }
        });
    });
});