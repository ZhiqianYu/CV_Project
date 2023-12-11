// 用户注册
document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('RegisterForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault(); // 阻止表单默认提交行为

            const formData = new FormData(registerForm);
            fetch('/register/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const username = data.username; // 后端返回的用户名

                    // 模拟异步请求延迟后弹出确认框
                    setTimeout(function() {
                        const confirmed = confirm(`注册成功！欢迎加入，${username}！`);
                        if (confirmed) {
                            // 如果用户点击确认，跳转到 homepage 页面
                            window.location.href = '/';
                        }
                    }, 500); // 模拟异步请求延迟
                } else {
                    alert('注册失败，请重试。');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});