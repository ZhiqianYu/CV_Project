document.addEventListener('DOMContentLoaded', function () {
    const frameRankButtons = document.querySelectorAll('.rank-btns');
    const rankNotif = document.getElementById('rank-notif');
    const choosedRankElement = document.getElementById('choosed-rank');
    const frameNumberElement = document.getElementById('choosed-frame-number');
    const frameTypeElement = document.getElementById('choosed-frame-type');
    const videoIdContainer = document.getElementById('video-id-container');
    const setSameRankBtn = document.getElementById('set-Same-Rank-Btn');

    let currentRating = null;
    let currentFrameType = null;
    let currentVideoId = null;

    function rateFrame(rating) {
        // 更新当前选择的评级和视频id
        currentRating = rating;
        currentVideoId = videoIdContainer.getAttribute('data-video-id');
        
        // 从页面中提取当前帧的类型和帧号
        const videoId = currentVideoId;
        const frameType = frameTypeElement.textContent;
        const frameNumber = frameNumberElement.textContent;

        fetch(`/annotate_frames/${videoId}/${frameType}/${frameNumber}/${currentRating}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                // 数据格式
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });

        rankNotif.style.display = 'block';

        setTimeout(function () {
            rankNotif.style.display = 'none';
        }, 1000);

        updateChoosedRank();
    }

    function setSameRankForSubframes() {
        // Get the current rating
        const currentRating = getCurrentRating();

        if (currentRating !== null) {
            // Get all 4-frame elements
            const frameElements4 = document.querySelectorAll('.frames-4 img');

            // Loop through each 4-frame element and set the same rating
            frameElements4.forEach(function (frameElement4) {
                const framePath4 = frameElement4.src;
                const frameNumber4 = extractFrameIndexFromPath(framePath4);
                const frameType4 = extractFrameTypeFromPath(framePath4);

                // Update the rating for the subframe
                rateSubframe(frameType4, frameNumber4, currentRating);
            });

            // Optionally, you can add a success message or perform other actions here
            console.log('Same rating set for all subframes.');
        } else {
            // Handle the case where no rating is selected
            console.error('No rating selected.');
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

    function getCurrentRating() {
        const ratingElement = document.getElementById('choosed-rank');
        if (ratingElement) {
            return ratingElement.textContent.trim();
        }
        return null;
    }

    function rateSubframe(frameType, frameNumber, rating) {

        currentVideoId = videoIdContainer.getAttribute('data-video-id');

        fetch(`/annotate_frames/${currentVideoId}/${frameType}/${frameNumber}/${rating}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                // Data format
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });

        rankNotif.style.display = 'block';

        setTimeout(function () {
            rankNotif.style.display = 'none';
        }, 1000);
    }

    function getCSRFToken() {
        const name = 'csrftoken=';
        const decodedCookie = decodeURIComponent(document.cookie);
        const cookieArray = decodedCookie.split(';');

        for (let i = 0; i < cookieArray.length; i++) {
            let cookie = cookieArray[i].trim();
            if (cookie.indexOf(name) == 0) {
                return cookie.substring(name.length, cookie.length);
            }
        }

        return null;
    }

    window.CSRF_TOKEN = getCSRFToken();

    // 更新提示信息区域内容
    function updateChoosedRank() {
        if (currentRating !== null && currentRating !== undefined && currentRating !== '') {
            choosedRankElement.textContent = `${currentRating}`;
        } else {
            choosedRankElement.textContent = `N/A`;
        }
    }

    // 为每个评级按钮添加点击事件监听器
    frameRankButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const rating = button.textContent.trim();
            rateFrame(rating);
        });
    });

    // 为设置相同评级按钮添加点击事件监听器
    setSameRankBtn.addEventListener('click', function () {
        setSameRankForSubframes();
    });

});
