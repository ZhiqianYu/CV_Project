function toggleCurrentPositionGenVisibility(show) {
    const currentPositionElement = document.querySelector('.current-position-gen');
    currentPositionElement.style.display = show ? 'block' : 'none';
}

function updateGenerationProgress(currentFrames, maxFrames) {
    const currentFrameElementGen = document.getElementById('current-Frame-gen');
    const maxFrameElementGen = document.getElementById('max_frame_number-gen');

    currentFrameElementGen.textContent = currentFrames;
    maxFrameElementGen.textContent = maxFrames;
}

function generateFrames(videoId) {
    // 弹出提示框
    var confirmation = confirm("Generate frames for the whole video?");

    // 处理用户的选择
    if (confirmation) {
        // 创建一个XMLHttpRequest对象
        var xhr = new XMLHttpRequest();

        // 配置请求
        xhr.open('GET', '/generate_frames/' + videoId + '/', true);

        // 设置回调函数，处理请求的结果
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    // Frame generation succeeded
                    alert("Frame generated and objects detected.");
                    window.location.reload();
                } else {
                    alert("Frame generation takes too long, try refresh the page: " + xhr.statusText);
                    window.location.reload();
                }
            }
        };

        // 发送请求
        xhr.send();
    } else {
        // 用户点击了“否”，在这里执行相应的操作或者什么都不做
        alert("Cancelled.");
    }
}