function handleUploadClick() {
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.click();
    }
}

function showFileName(input) {
    const file = input.files[0];
    const fileNameArea = document.getElementById('fileNameArea');
    const chooseFileBtn = document.getElementById('chooseFileBtn');
    const UploadFileBtn = document.getElementById('uploadFileBtn');

    if (file) {
        fileNameArea.textContent = 'File: ' + file.name;
        fileNameArea.style.display = 'block';
        // 选择文件后，显示内容变更为更改文件, 显示上传按钮
        chooseFileBtn.textContent = 'Change File';
        UploadFileBtn.style.display = '';
    }
}

function uploadFile() {
    var form = document.getElementById('UploadForm');
    var formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => handleUploadResponse(data))
    .catch((error) => {
        console.error('Error:', error);
    });
}

function handleUploadResponse(response) {
    if (response.status === 'Upload Success' && response.message === 'File uploaded. Database and preview created.') {
        var uploadAnother = confirm('File uploaded. Database and preview created. Do you want to upload another file?');
        if (uploadAnother) {
            // 清空文件输入框
            document.getElementById('fileInput').value = '';
            // 清空文件名显示区域
            document.getElementById('fileNameArea').textContent = '';
            document.getElementById('fileNameArea').style.display = 'none';
            // 恢复按钮状态
            document.getElementById('chooseFileBtn').textContent = 'Choose File';
            document.querySelector('button[type="button"]').style.display = 'none';
        } else {
            window.location.href = 'videos';
        }
    } else if (response.status === 'Upload Success' && response.message === 'File exist, database updated, preview created.') {
        alert('File exist, database updated, preview created.');
        window.location.href = '/';
    } else if (response.status === 'Upload Success' && response.message === 'Files exist, database updated.') {
        alert('Files exist, database updated. No need to upload.');
        window.location.href = '/';
    } else if (response.status === 'Upload Success') {
        var uploadAnother = confirm('Upload Success! Do you want to upload another file?');
        if (uploadAnother) {
            // 清空文件输入框
            document.getElementById('fileInput').value = '';
            // 清空文件名显示区域
            document.getElementById('fileNameArea').textContent = '';
            document.getElementById('fileNameArea').style.display = 'none';
            // 恢复按钮状态
            document.getElementById('chooseFileBtn').textContent = 'Choose File';
            document.querySelector('button[type="button"]').style.display = 'none';
        } else {
            window.location.href = 'videos';
        }
    } else {
        alert('Upload Failed: ' + response.message);
        window.location.href = '/';
    }
}
