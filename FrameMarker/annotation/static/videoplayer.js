/* play btn */
document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('VideoLoaded');
    const playPauseBtn = document.getElementById('playPauseBtn');

    playPauseBtn.addEventListener('click', function () {
        if (video.paused) {
            video.play();
            playPauseBtn.innerText = 'Pause';
        } else {
            video.pause();
            playPauseBtn.innerText = 'Play';
        }
    });
});

/* progress bar */
// 获取相关的元素
const progressBar = document.getElementById('progressBar');
const progressIndicator = document.getElementById('progressIndicator');
const currentFrameElement = document.getElementById('currentFrame');
const totalFramesElement = document.getElementById('totalFrames');
const currentTimeElement = document.getElementById('currentTime');
const totalTimeElement = document.getElementById('totalTime');
const videoPlayer = document.getElementById('VideoLoaded');

// 监听视频加载事件，更新总帧数和总时间
videoPlayer.addEventListener('loadedmetadata', () => {
    // 设置总帧数和总时间
    const totalFrames = Math.floor(videoPlayer.duration * videoPlayer.playbackRate * 60);
    const totalTime = formatTime(videoPlayer.duration);

    // 更新 HTML 元素
    totalFramesElement.textContent = totalFrames;
    totalTimeElement.textContent = totalTime;
});

// 监听视频播放事件，更新进度条和信息
videoPlayer.addEventListener('timeupdate', updateProgress);

// 更新进度条和信息的函数
function updateProgress() {
    // 计算进度条位置
    const progress = (videoPlayer.currentTime / videoPlayer.duration) * 100;
    progressBar.style.width = `${progress}%`;
    progressIndicator.style.left = `${progress}%`;

    // 更新当前帧
    const currentFrame = Math.floor(videoPlayer.currentTime * videoPlayer.playbackRate * 60);
    currentFrameElement.textContent = currentFrame;

    // 更新当前时间
    const currentTime = formatTime(videoPlayer.currentTime);
    currentTimeElement.textContent = currentTime;
}

// 格式化时间的函数
function formatTime(timeInSeconds) {
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = Math.floor(timeInSeconds % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
}

// 点击进度条时跳转到对应位置
function updateProgressBar(event) {
    const progressBarRect = progressBar.getBoundingClientRect();
    const clickPosition = event.clientX - progressBarRect.left;
    const percentage = (clickPosition / progressBarRect.width) * 100;
    const newPosition = (percentage / 100) * videoPlayer.duration;
    videoPlayer.currentTime = newPosition;
}
