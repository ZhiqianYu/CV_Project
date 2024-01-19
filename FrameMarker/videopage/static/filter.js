document.addEventListener('DOMContentLoaded', function (){
    
    var filterForm = document.getElementById('filterForm');
    
    
    filterForm.addEventListener('submit', function (event) {
        event.preventDefault();

        var formData = new FormData(filterForm);

        var xhr = new XMLHttpRequest();
        xhr.open('GET', filterForm.action + '?' + new URLSearchParams(formData).toString(), true);
        xhr.onload = function () {
            if (xhr.status === 200) {
    
                var response = JSON.parse(xhr.responseText);
                document.getElementById('videoList').innerHTML = response;
            } else {
                console.error('Error:', xhr.statusText);
            }
        };
        xhr.send();
    });

});

