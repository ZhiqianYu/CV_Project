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
