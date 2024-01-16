document.addEventListener('DOMContentLoaded', function () {
    const videoPlayerContainer = document.querySelector('.video-player');
    const frameElements = document.querySelectorAll('.frames-60 img');
    const choosedFrameNumberElement = document.getElementById('choosed-frame-number');
    const progressIndicator = document.getElementById('progressIndicator');
    const currentFrameElement = document.getElementById('current-Frame');
    const totalFramesElement = document.getElementById('max_frame_number');
    const video = document.getElementById('VideoLoaded');
    const playPauseBtn = document.getElementById('playPauseBtn');

    let totalFrames = parseInt(totalFramesElement.textContent);
    let selectedFrameNumber = null;
    let isFrameSelected = false;

    function displaySelectedFrame(framePath) {
        const frameIndex = extractFrameIndexFromPath(framePath);
        selectedFrameNumber = frameIndex;
        choosedFrameNumberElement.textContent = selectedFrameNumber;
        updateProgressBar();
        updateVideoPlayer(framePath);
    }

    function updateProgressBar() {
        if (isFrameSelected) {
            const percentage = (selectedFrameNumber / totalFrames) * 100;
            progressIndicator.style.width = percentage + '%';
            currentFrameElement.textContent = selectedFrameNumber;
        } else {
            progressIndicator.style.width = '0%';
            currentFrameElement.textContent = '0';
        }
    }

    function updateVideoPlayer(framePath) {
        // Clear the contents of the video player container
        videoPlayerContainer.innerHTML = '';

        if (isFrameSelected) {
            // Create a new img element
            const imgElement = document.createElement('img');
            imgElement.src = framePath;
            imgElement.alt = 'choosed-frame';

            // Append the img element to the video player container
            videoPlayerContainer.appendChild(imgElement);
        } else {
            // If no frame is selected, restore the original video
            const videoPlayer = document.createElement('video');
            videoPlayer.id = 'VideoLoaded';
            videoPlayer.controls = 'false';

            const sourceElement = document.createElement('source');
            sourceElement.src = '{{ MEDIA_URL }}{{ video.video_file }}';
            sourceElement.type = 'video/mp4';

            videoPlayer.appendChild(sourceElement);
            videoPlayerContainer.appendChild(videoPlayer);
        }
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
            isFrameSelected = true;
            displaySelectedFrame(framePath);
        });
    });

    // Add an event listener to the video player container to handle clicks on blank space
    videoPlayerContainer.addEventListener('click', function () {
        isFrameSelected = false;
        selectedFrameNumber = null;
        choosedFrameNumberElement.textContent = '0';
        updateProgressBar();
        updateVideoPlayer();
    });

    playPauseBtn.addEventListener('click', function () {
        // Check if videoPlayerContainer contains an img element (frame image)
        const containsFrameImage = videoPlayerContainer.querySelector('img') !== null;

        if (containsFrameImage) {
            // If frame image is present, clear the container and load the video
            videoPlayerContainer.innerHTML = '';
            videoPlayerContainer.appendChild(video);
        } else {
            // If no frame image, toggle play/pause of the video
            if (video.paused) {
                video.play();
                playPauseBtn.innerText = 'Pause';
            } else {
                video.pause();
                playPauseBtn.innerText = 'Play';
            }
        }
    });
});
