document.addEventListener("DOMContentLoaded", function () {
    var exportButton = document.getElementById("exportBtn");
    var videoId = document.getElementById("videoSelect").value;

    if (exportButton) {
        exportButton.addEventListener("click", function() {
            exportAnnotations(videoId);
        });
    }

    function exportAnnotations(videoId) {
        var selectedFormats = document.querySelectorAll('input[name="format"]:checked');
        var selectedColumns = document.querySelectorAll('.column-checkbox:checked');

        selectedFormats.forEach(function (format) {
            // Combine selected columns into a single array
            var selectedColumnsArray = Array.from(selectedColumns).map(function (column) {
                return column.value;
            });

            // Assuming you have the video_id available in your HTML, replace 'your_video_id' with the actual value
            var videoID = videoId;

            // Form the URL based on the selected format and columns
            var url = `/export/${format.value}/${videoID}?columns=${selectedColumnsArray.join(',')}`;

            // Create a hidden link element and trigger a click event to download the file
            var link = document.createElement('a');
            link.href = url;
            link.download = `${format.value}_${videoID}.${format.value === 'json' ? 'json' : 'csv'}`;
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }
});