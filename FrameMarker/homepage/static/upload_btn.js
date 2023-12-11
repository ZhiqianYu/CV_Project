document.getElementById('upload-button').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('file-upload').click();
});

document.getElementById('file-upload').addEventListener('change', function() {
    document.getElementById('file-name').textContent = this.files[0].name;
    document.getElementById('file-info').style.display = 'block';
});

document.getElementById('confirm-button').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('file-info').style.display = 'none';
    document.getElementById('upload-button').form.submit();
});