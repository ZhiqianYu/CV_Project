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

    async function rateFrame(rating) {
        // Update current selection and video id
        currentRating = rating;
        currentVideoId = videoIdContainer.getAttribute('data-video-id');
        
        // Extract current frame information
        const videoId = currentVideoId;
        const frameType = frameTypeElement.textContent;
        const frameNumber = frameNumberElement.textContent;

        try {
            const response = await fetch(`/annotate_frames/${videoId}/${frameType}/${frameNumber}/${currentRating}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({
                    // Data format
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            console.log(data);

            rankNotif.style.display = 'block';

            setTimeout(function () {
                rankNotif.style.display = 'none';
            }, 1000);

            updateChoosedRank();

            // Fetch updated overlay content after rating, only if the rating action was successful
            if (data.status === 'success') {
                if (frameType === '60') {
                    await updateOverlayInformation();
                } else if (frameType === '4') {
                    await fetchAndLoadSubOverlayInfo(currentVideoId, frameType, frameNumber);
                }
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async function updateOverlayInformation() {
        await fetchUpdatedOverlayData();
    }

    async function fetchUpdatedOverlayData() {
        // Fetch updated overlay data from the server
        const currentVideoId = videoIdContainer.getAttribute('data-video-id');
        try {
            const response = await fetch(`/update_overlay/${currentVideoId}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            // Handle the updated data and update overlay content
            updateOverlayContent(data.frame_info_list);
        } catch (error) {
            console.error('Error fetching updated data:', error);
        }
    }

    function updateOverlayContent(FrameInfoList) {
        // Update overlay-a-top content based on the fetched data
        const overlayATopElements = document.querySelectorAll('.overlay-a-top');
    
        overlayATopElements.forEach(function (overlayATopElement, index) {
            const FrameInfo = FrameInfoList[index];
    
            // Find child elements within overlay-a-top
            const annoInfoElement = overlayATopElement.querySelector('.anno-info');
            const annoRankElement = overlayATopElement.querySelector('.anno-rank');
    
            // Update content based on FrameInfo properties
            if (FrameInfo) {
                if (FrameInfo.annotation) {
                    // Update annotation information
                    annoInfoElement.innerHTML = FrameInfo.annotation.is_annotated ? '✅' : '⚠️';
                    annoRankElement.innerHTML = FrameInfo.annotation.rank ? FrameInfo.annotation.rank : '';
                } else {
                    // Handle the case when there is no annotation
                    annoInfoElement.innerHTML = '';
                    annoRankElement.innerHTML = '';
                }
            } else {
                // Handle the case when FrameInfo is not available
                annoInfoElement.innerHTML = '';
                annoRankElement.innerHTML = '';
            }
        });
    }

    function setSameRankForSubframes() {
        // Get the current rating
        const currentRating = getCurrentRating();
    
        // Get the frame type and number elements
        const frameNumberElement = document.getElementById('choosed-frame-number');
        const frameTypeElement = document.getElementById('choosed-frame-type');
    
        if (currentRating !== null) {
            // Get the frame type
            const frameType = frameTypeElement.textContent.trim();
    
            // Check if the chosen frame is a 60 frame
            if (frameType === '60') {
                // Get the frame number
                const frameNumber = parseInt(frameNumberElement.textContent.trim());
    
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
    
                // Display rank notification
                rankNotif.style.display = 'block';

                setTimeout(function () {
                    rankNotif.style.display = 'none';
                }, 1000);

                // Reload 4 frames for the corresponding 60 frame, place here to ensure the rating is updated
                fetchAndLoad4Frames(frameNumber);
                console.log('Subframes rated and loaded for the selected main frame.');
            } else {
                // If the chosen frame is not a 60 frame, show an error message
                console.error('Please select a main frame to rate subframes.');
                alert('Please select a main frame to rate subframes.');
            }
        } else {
            // If no rating is selected, show an error message
            console.error('No rating selected.');
            alert('Please select a rating before applying to subframes.');
        }
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
