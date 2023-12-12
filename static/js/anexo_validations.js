
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

const form = document.getElementById('form1');
form.addEventListener('submit', (event) => {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    const maxSizeInBytes = 5 * 1024 * 1024; // 5 MB

    for (const input of fileInputs) {
        if (!validarTamanioArchivo(input, maxSizeInBytes)) {
            event.preventDefault();
            return;
        }
    }
});

const fileInputs = document.querySelectorAll('input[type="file"]');
const maxSizeInBytes = 5 * 1024 * 1024; // 5 MB

fileInputs.forEach(input => {
    input.addEventListener('change', () => {
        validarTamanioArchivo(input, maxSizeInBytes);
    });
});
