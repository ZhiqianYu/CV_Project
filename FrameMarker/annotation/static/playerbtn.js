// playbtn
document.getElementById('playBtn').addEventListener('click', function() {
    document.getElementById('buttonStatus').innerText = 'Button: Play';
});

// resumebtn
document.getElementById('resumeBtn').addEventListener('click', function() {
    document.getElementById('buttonStatus').innerText = 'Button: Resume';
});

// selectbtn
document.getElementById('selectBtn').addEventListener('click', function() {
    document.getElementById('buttonStatus').innerText = 'Button: Select Video';
});

// exportbtn
document.getElementById('exportBtn').addEventListener('click', function() {
    document.getElementById('buttonStatus').innerText = 'Button: Export';
});