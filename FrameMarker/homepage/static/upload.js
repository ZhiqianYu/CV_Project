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
            window.location.href = 'videos'; // 上传成功后跳转到videos页面, 与url的path相同
        }
    } else if (response.status === 'Upload Failed') {
        alert('文件上传失败：' + response.message);
    }
}
