document.addEventListener('mousemove', function (e) {
    const ripple = document.createElement('div');
    ripple.classList.add('ripple');
    ripple.style.top = e.clientY - 25 + 'px';
    ripple.style.left = e.clientX - 25 + 'px';

    const barRect = document.querySelector('.navbar').getBoundingClientRect();
    const isInsideBar = e.clientX >= barRect.left && e.clientX <= barRect.right &&
                        e.clientY >= barRect.top && e.clientY <= barRect.bottom;

    if (!isInsideBar) {
        document.body.appendChild(ripple);
        setTimeout(() => {
            ripple.remove();
        }, 200);
    }
});