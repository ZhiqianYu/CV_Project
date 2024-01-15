function chooseFrame(framePath) {
    // 获取选择的帧的文件名的最后一个_后面的数字
    const choosedFrameNumber = framePath.split('_').pop().split('.')[0];

    // 更新页面中的 Choosed Frame 显示
    document.getElementById('choosed-frame-number').textContent = choosedFrameNumber;

    // 移除之前选择的帧的边框样式
    const previousChoosedFrame = document.querySelector('.frames-60 .choosed');
    if (previousChoosedFrame) {
        previousChoosedFrame.classList.remove('choosed');
    }

    // 获取选择的帧图像元素并添加边框和样式
    const choosedFrameImg = document.querySelector(`.frames-60 img[src="${framePath}"]`);
    choosedFrameImg.classList.add('choosed');

    // 更新选择的帧图像
    document.getElementById('choosed-frame-img').src = framePath;
}

function updateProgressBar(event) {
    const progressBar = document.getElementById('progressBar');
    const progressIndicator = document.getElementById('progressIndicator');
    const currentFrameElement = document.getElementById('currentFrame');
    const totalFramesElement = document.getElementById('totalFrames');

    // 获取鼠标点击位置相对于进度条的百分比
    const clickPercentage = (event.offsetX / progressBar.clientWidth) * 100;

    // 计算对应的帧数
    const totalFrames = parseInt(totalFramesElement.textContent);
    const currentFrame = Math.floor((clickPercentage / 100) * totalFrames);

    // 更新当前帧数
    currentFrameElement.textContent = currentFrame;

    // 更新进度条位置
    progressIndicator.style.width = `${clickPercentage}%`;
}

document.addEventListener('DOMContentLoaded', function () {
    const frameImages = document.querySelectorAll('.frames-60 img');

    frameImages.forEach(function (img) {
        img.addEventListener('click', function () {
            const framePath = img.getAttribute('src');
            chooseFrame(framePath);
        });
    });
});

function displaySelectedFrame(framePath, frameNumber, totalFrames) {
    const videoPlayer = document.getElementById('VideoLoaded');
    const selectedFrame = document.getElementById('selectedFrame');

    // 如果存在 selectedFrame 元素，则显示帧图像
    if (selectedFrame) {
        selectedFrame.src = framePath;
        videoPlayer.style.display = 'none';  // 隐藏视频播放器
        selectedFrame.style.display = 'block';  // 显示帧图像
    }

    // 更新当前帧数和总帧数
    const currentFrameElement = document.getElementById('currentFrame');
    const totalFramesElement = document.getElementById('totalFrames');
    currentFrameElement.textContent = frameNumber;
    totalFramesElement.textContent = totalFrames;
}