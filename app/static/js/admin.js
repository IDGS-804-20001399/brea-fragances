const swal = Swal.mixin({
  customClass: {
    confirmButton: 'btn btn-success me-3',
    cancelButton: 'btn btn-danger'
  },
  buttonsStyling: false
})

document.querySelector('input[type=file].image')?.addEventListener('change', (e) => {
    const reader = new FileReader();
    reader.onload = () => {
        const previewImg = e.target.parentElement.querySelector('img.preview');
        previewImg.setAttribute('src', reader.result);
    }
    reader.readAsDataURL(e.target.files[0]);
});

document.querySelectorAll('form.delete').forEach(f => {
    f.addEventListener('submit', async (e) => {
        e.preventDefault();
        const response = await swal.fire({
            icon: 'warning',
            title: 'Delete record',
            text: 'Do you want to delete the selected record?',
            confirmButtonText: 'Yes',
            focusCancel: true,
            showCancelButton: true
        })
        if (response.isConfirmed){
            f.submit()
        }
    });
})