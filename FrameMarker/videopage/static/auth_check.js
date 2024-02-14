// auth_check.js

(function () {
    // Check if the user is authenticated
    if (!{{ user.is_authenticated|yesno:"true,false" }}) {
        alert('Please log in to view the content.');
        window.location.href = '/login/';
    }
})();