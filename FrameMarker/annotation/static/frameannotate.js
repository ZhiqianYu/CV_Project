document.addEventListener('DOMContentLoaded', function () {
    const frameRankButtons = document.querySelectorAll('.rank-btns');
    const rankNotif = document.getElementById('rank-notif');
    const choosedRankElement = document.getElementById('choosed-rank');
    const frameNumberElement = document.getElementById('choosed-frame-number');
    const frameTypeElement = document.getElementById('choosed-frame-type');
    const videoIdContainer = document.getElementById('video-id-container');

    let currentRating = null;
    let currentFrameType = null;
    let currentVideoId = null;

    function rateFrame(rating) {
        // 更新当前选择的评级和视频id
        currentRating = rating === 'Clear' ? '' : rating;
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

    // Add the CSRF token to the global scope so that it can be accessed in your frameannotate.js
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

});
