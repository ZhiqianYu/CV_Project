function showFileName(input) {
    const file = input.files[0];
    const fileNameArea = document.getElementById('fileNameArea');
    const chooseFileBtn = document.getElementById('chooseFileBtn');
    const uploadButton = document.querySelector('button[type="button"]');

    if (file) {
        fileNameArea.textContent = 'Selected File: ' + file.name;
        fileNameArea.style.display = 'block';
        chooseFileBtn.textContent = 'Change File';
        uploadButton.style.display = 'inline-block';
    }
}


function uploadFile() {
    var form = document.getElementById('uploadForm');
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

// 处理response返回值
function handleUploadResponse(response) {
    if (response.status === 'Upload Success') {
        var uploadAnother = confirm('视频成功上传，是否上传另一个视频？');
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
            window.location.href = '/videopage/';
        }
    } else if (response.status === 'Upload Failed') {
        alert('文件上传失败：' + response.message);
    }
}
