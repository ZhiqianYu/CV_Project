document.addEventListener('DOMContentLoaded', function () {
    const videoPlayerContainer = document.querySelector('.video-player');
    const frameElements60 = document.querySelectorAll('.frames-60 img');
    const frameElements4 = document.querySelectorAll('.frames-4 img');
    
    // 鼠标悬浮状态保持
    const frameContainers60 = document.querySelectorAll('.frames-60');
    const frameContainers4 = document.querySelectorAll('.frames-4');

    // 所选帧的信息更新到页面
    const choosedFrameNumberElement = document.getElementById('choosed-frame-number');
    const choosedFrameTypElement = document.getElementById('choosed-frame-type');
    const choosedFrameElement = document.querySelector('.choosed-frame');
    
    // 进度条更新到页面
    const progressIndicator = document.getElementById('progressIndicator');
    const currentFrameElement = document.getElementById('current-Frame');
    const totalFramesElement = document.getElementById('max_frame_number');

    // 视频播放器按钮
    const video = document.getElementById('VideoLoaded');
    const playPauseBtn = document.getElementById('playPauseBtn');

    const framesContainer60 = document.querySelector('.frames-container');
    const framesContainer4 = document.querySelector('.frames-container-4');

    // 帧图像窗口滚动控制
    const scrollHeight60 = 404;
    const scrollHeight4 = 240;
    

    let totalFrames = parseInt(totalFramesElement.textContent);
    let selectedFrameNumber = null;
    let selectedFrameTyp = null;
    let isFrameSelected = false;

    function displaySelectedFrame(framePath) {
        const frameIndex = extractFrameIndexFromPath(framePath);
        const frameType = extractFrameTypeFromPath(framePath);
        selectedFrameNumber = frameIndex;
        selectedFrameTyp = frameType;
        choosedFrameNumberElement.textContent = selectedFrameNumber;
        choosedFrameTypElement.textContent = selectedFrameTyp;

        // Save frame type to a custom attribute in an element
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

    function extractFrameTypeFromPath(framePath) {
        const matches = framePath.match(/\/(\d+)\/frame_(\w+)_\d+(_\d+)?\.png/);
        if (matches && matches[2]) {
            return matches[2];
        }
        return '';  // Default to empty string if no match
    }

    function extract4PathFrom60Path(framePath) {
        // Extract the base path for 4-frame paths from the 60-frame path
        const basePath0 = framePath.substring(0, framePath.lastIndexOf('/'));
        const basePath = framePath.substring(0, basePath0.lastIndexOf('/'));
        return `${basePath}/4`;
    }

    function fetchAndLoad4Frames(selectedFrameIndex) {
        // Simulate fetching 4-frame paths
        const framePaths4 = simulateFetching4Frames(selectedFrameIndex);

        // Update the HTML to include the fetched 4-frame paths dynamically
        updateFramesContainer4(framePaths4);
    }

    function simulateFetching4Frames(selectedFrameIndex) {
        // Fetching 4-frame paths from the server based on the selected 60-frame index
        const framePaths4 = [];
        for (let i = selectedFrameIndex + 4; i < selectedFrameIndex + 60 && i < totalFrames; i += 4) {
            const framePath4 = `${extract4PathFrom60Path(frameElements60[0].src)}/frame_4_${i}.png`;
            framePaths4.push(framePath4);
        }
        return framePaths4;
    }

    function updateFramesContainer4(framePaths4) {
        // Clear the existing content in the 4-frames container
        framesContainer4.innerHTML = '';
    
        // Append the fetched 4-frame paths to the 4-frames container
        for (const framePath4 of framePaths4) {
            const frameElement4 = document.createElement('div');
            frameElement4.classList.add('frames-4');
    
            const imgElement4 = document.createElement('img');
            imgElement4.src = framePath4;
            imgElement4.alt = 'frame';
    
            frameElement4.appendChild(imgElement4);
            framesContainer4.appendChild(frameElement4);
        }
    
        // Reattach event listeners for the 4 frames
        attachedEventListenersTo4Frames();
    }

    // event listener for the 60 frames
    frameElements60.forEach((frameElement) => {
        frameElement.addEventListener('click', function () {
            const framePath = frameElement.src;
            isFrameSelected = true;
            displaySelectedFrame(framePath);

            const selectedFrameIndex = extractFrameIndexFromPath(framePath);
            fetchAndLoad4Frames(selectedFrameIndex);
        });
    });

    // event listener for the 4 frames
    function attachedEventListenersTo4Frames() {
        // Get the updated frame elements after reattaching the HTML
        const frameElements4Updated = document.querySelectorAll('.frames-4 img');
    
        // Event listener for the 4 frames
        frameElements4Updated.forEach((frameElement4) => {
            frameElement4.addEventListener('click', function () {
                const framePath4 = frameElement4.src;
                isFrameSelected = true;

                removeClickedClassFrom60Frames();
                removeClickedClassFrom4Frames();
                displaySelectedFrame(framePath4);
                frameElement4.parentElement.classList.add('frame-clicked');
            });
        });
    }

    function removeClickedClassFrom60Frames() {
        frameContainers60.forEach(function (container) {
            container.classList.remove('frame-clicked');
        });
    }

    function removeClickedClassFrom4Frames() {
        const allFrames4 = document.querySelectorAll('.frames-4');
        allFrames4.forEach(function (container) {
            container.classList.remove('frame-clicked');
        });
    }

    // event listener to the video player container to handle clicks on blank space
    videoPlayerContainer.addEventListener('click', function () {
        isFrameSelected = false;
        selectedFrameNumber = null;
        choosedFrameNumberElement.textContent = '0';
        updateProgressBar();
        updateVideoPlayer();
    });

    // event listener to the video player container to handle clicks on blank space
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

    // event listener to scroll height 60
    framesContainer60.addEventListener('wheel', function (event) {
        // 禁止默认的滚动行为，防止页面整体滚动
        event.preventDefault();
    
        // 根据滚动方向调整滚动位置
        if (event.deltaY > 0) {
            framesContainer60.scrollTop += scrollHeight60;
        } else {
            framesContainer60.scrollTop -= scrollHeight60;
        }
    });

    // event listener to scroll height 4
    framesContainer4.addEventListener('wheel', function (event) {
        // 禁止默认的滚动行为，防止页面整体滚动
        event.preventDefault();
    
        // 根据滚动方向调整滚动位置
        if (event.deltaY > 0) {
            framesContainer4.scrollTop += scrollHeight4;
        } else {
            framesContainer4.scrollTop -= scrollHeight4;
        }
    });

    // 为每个元素添加点击事件监听器
    frameContainers60.forEach(function (container) {
        container.addEventListener('click', function () {
            removeClickedClassFrom60Frames();
            container.classList.add('frame-clicked');
        });
    });
});
