// auth_check.js

document.addEventListener("DOMContentLoaded", function() {
    // 获取用户登录状态
    var isAuthenticated = document.getElementById("auth-check").getAttribute("data-is-authenticated");

    if (!isAuthenticated) {
        // 用户未登录时的处理逻辑
        alert('Please log in to access this page.');
        window.location.href = '/login/';
    }
});
