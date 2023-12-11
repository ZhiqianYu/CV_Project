$(document).ready(function(){
    $("form").on("submit", function(event){
        event.preventDefault();

        var formData = new FormData(this);

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: formData,
            processData: false,
            contentType: false,
            success: function(response){
                // 检查服务器返回的状态
                if (response.status === 'Upload Success') {
                    // 如果上传成功，你可以在这里做一些事情，例如显示一个成功的消息
                    var uploadAnother = confirm('视频成功上传，是否上传另一个视频？');
                    if (uploadAnother) {
                        // 清空文件输入框
                        document.getElementById('file-upload').value = '';
                    } else {
                        // 重定向到 videopage
                        window.location.href = '/videopage/';
                    }
                } else if (response.status === 'Upload Failed') {
                    // 如果上传失败，你可以在这里做一些事情，例如显示一个错误消息
                    alert('文件上传失败：' + response.message);
                }
            }
        });
    });
});