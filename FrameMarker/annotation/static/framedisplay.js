document.addEventListener('DOMContentLoaded', function () {
    const videoPlayerContainer = document.querySelector('.video-player');
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
        // Create a new img element
        const imgElement = document.createElement('img');
        imgElement.src = framePath;
        imgElement.alt = 'choosed-frame';

        // Clear the contents of the video player container
        videoPlayerContainer.innerHTML = '';

        // Append the img element to the video player container
        videoPlayerContainer.appendChild(imgElement);
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
