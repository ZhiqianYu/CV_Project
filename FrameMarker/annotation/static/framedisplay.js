document.addEventListener('DOMContentLoaded', function () {
    const videoPlayer = document.getElementById('VideoLoaded');
    const frameElements = document.querySelectorAll('.frames-60 img');
    const choosedFrameNumberElement = document.getElementById('choosed-frame-number');
    const progressIndicator = document.getElementById('progressIndicator');
    const currentFrameElement = document.getElementById('current-Frame');
    const totalFramesElement = document.getElementById('max_frame_number');

    let totalFrames = parseInt(totalFramesElement.textContent);
    let selectedFrameNumber = 0;

    function displaySelectedFrame(framePath) {
        const frameIndex = extractFrameIndexFromPath(framePath);
        selectedFrameNumber = frameIndex;
        choosedFrameNumberElement.textContent = selectedFrameNumber;
        updateProgressBar();
        updateVideoPlayer(framePath);
    }

    function updateProgressBar() {
        const percentage = (selectedFrameNumber / totalFrames) * 100;
        progressIndicator.style.width = percentage + '%';
        currentFrameElement.textContent = selectedFrameNumber;
    }

    function updateVideoPlayer(framePath) {
        videoPlayer.style.display = 'none';
        videoPlayer.pause();
        videoPlayer.src = framePath;
        videoPlayer.load();
        videoPlayer.style.display = 'block';
    }

    function extractFrameIndexFromPath(framePath) {
        // Extract the last number after the last underscore in the frame filename
        const matches = framePath.match(/_(\d+)\.png/);
        if (matches && matches[1]) {
            return parseInt(matches[1]);
        }
        return 0;  // Default to 0 if no match
    }

    frameElements.forEach((frameElement) => {
        frameElement.addEventListener('click', function () {
            const framePath = frameElement.src;
            displaySelectedFrame(framePath);
        });
    });
});