document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('.export-button').addEventListener('click', function () {
        const frameAnnotations = JSON.parse("{{ frame_annotations_json|safe }}");
        exportAnnotations(frameAnnotations);
    });

    function exportAnnotations(frameAnnotations) {
        // The frameAnnotations variable contains the data from the Django view
        // Now you can use frameAnnotations for your export logic
        console.log('Frame Annotations Data:', frameAnnotations);
        // ...
    }

    // Add your additional functions or modifications here if needed.
});
