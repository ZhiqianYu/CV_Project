// 遍历 videoData 数组，将每个视频的信息渲染到页面中对应的视频框中
videoData.forEach((video, index) => {
    const videoItem = document.getElementsByClassName('video-item')[index];
    const placeholderImg = videoItem.querySelector('.placeholder-img');
    const placeholderDetailTitle = videoItem.querySelector('.placeholder-detail-title');
    const placeholderDetailUser = videoItem.querySelector('.placeholder-detail-user');
    
    // 将占位符图像替换为视频的实际预览图像
    placeholderImg.style.backgroundImage = `url(${video.previewImageURL})`;
    
    // 将占位符文本信息替换为视频的实际标题和用户信息
    placeholderDetailTitle.textContent = video.title;
    placeholderDetailUser.textContent = video.user;
});