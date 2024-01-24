document.addEventListener("DOMContentLoaded", function () {
    var exportButton = document.getElementById("exportBtn");
    console.log("frameAnnotationsJson:", frameAnnotationsJson);

    if (exportButton) {
        exportButton.addEventListener("click", exportAnnotations);
    }

    function exportAnnotations() {
        var selectedFormats = [];

        // Check if JSON format is selected
        if (document.getElementById("jsonCheckbox").checked) {
            selectedFormats.push("json");
        }

        // Check if CSV format is selected
        if (document.getElementById("csvCheckbox").checked) {
            selectedFormats.push("csv");
        }

        // Validate that at least one format is selected
        if (selectedFormats.length === 0) {
            alert("Please select at least one format for export.");
            return;
        }

        // Generate file content based on selected formats
        if (selectedFormats.includes("json")) {
            downloadFile(JSON.stringify(frameAnnotationsJson, null, 2), "frame_annotations", "json");
        }

        if (selectedFormats.includes("csv")) {
            // Convert to CSV and download
            var csvContent = convertToCSV(frameAnnotationsJson);
            downloadFile(csvContent, "frame_annotations", "csv");
        }
    }

    function convertToCSV(data) {
        var csv = "";
        var columns = Object.keys(data[0]);

        // Add header row
        csv += columns.join(",") + "\n";

        // Add data rows
        data.forEach(function (row) {
            var values = columns.map(function (column) {
                return row[column];
            });
            csv += values.join(",") + "\n";
        });

        return csv;
    }

    function downloadFile(content, fileName, format) {
        var blob = new Blob([content], { type: "text/" + format });
        var link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = fileName + "." + format;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
});
