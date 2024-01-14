// Get the video element and the play/pause button
const video = document.getElementById("video_{{ video.id }}"); // Replace "your_video_id" with your actual video element ID
const playPauseBtn = document.getElementById("playPauseBtn");

// Add event listener for the play/pause button
playPauseBtn.addEventListener("click", function() {
    if (video.paused || video.ended) {
        // If video is paused or ended, play it
        video.play();
        playPauseBtn.textContent = "Pause";
    } else {
        // If video is playing, pause it
        video.pause();
        playPauseBtn.textContent = "Play";
    }
});

// Update the play/pause button text when video playback state changes
video.addEventListener("play", function() {
    playPauseBtn.textContent = "Pause";
});

video.addEventListener("pause", function() {
    playPauseBtn.textContent = "Play";
});

video.addEventListener("ended", function() {
    playPauseBtn.textContent = "Play";
});
