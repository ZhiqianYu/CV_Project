function generateFrames(videoId) {
    // 弹出提示框
    var confirmation = confirm("Would you like to generate frames for the whole video file?");

    // 处理用户的选择
    if (confirmation) {
        // 用户点击了“是”，执行帧图像生成
        // 创建一个XMLHttpRequest对象
        var xhr = new XMLHttpRequest();
        
        // 配置请求
        xhr.open('GET', '/generate_frames/' + videoId + '/', true);
        
        // 设置回调函数，处理请求的结果
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    alert("Frame generated!");
                } else {
                    console.error("Frame generation failed:", xhr.statusText);
                }
            }
        };
        
        // 发送请求
        xhr.send();
    } else {
        // 用户点击了“否”，在这里执行相应的操作或者什么都不做
        alert("Canceled.");
    }
}