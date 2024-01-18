
function submitForm() {
    var formData = new FormData(document.getElementById('filterForm'));

    var xhr = new XMLHttpRequest();
    xhr.open('GET', "{% url 'video_list' %}?" + new URLSearchParams(formData).toString(), true);
    xhr.onload = function () {
        console.log(xhr.responseText);
    };
    xhr.send();
}
