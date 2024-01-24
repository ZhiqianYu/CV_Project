document.addEventListener('DOMContentLoaded', function () {
    let isAsc = true;

    function sortTable(column) {
        const tbody = document.querySelector('.annotation-table tbody');

        const rows = Array.from(tbody.querySelectorAll('tr'));

        rows.sort((a, b) => {
            const aValue = a.dataset[column];
            const bValue = b.dataset[column];

            if (aValue < bValue) return isAsc ? -1 : 1;
            if (aValue > bValue) return isAsc ? 1 : -1;
            return 0;
        });

        rows.forEach(row => tbody.appendChild(row));

        isAsc = !isAsc;
    }

    document.querySelector('.annotation-table').addEventListener('click', function (event) {
        if (event.target.classList.contains('sortable')) {
            const column = event.target.dataset.column;

            document.querySelectorAll('.sortable').forEach(header => header.classList.remove('sorted-asc', 'sorted-desc'));
            event.target.classList.add(isAsc ? 'sorted-asc' : 'sorted-desc');

            sortTable(column);
        }
    });

    function exportData(format) {
        const tbody = document.querySelector('.annotation-table tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));

        const data = [];

        rows.forEach(row => {
            const rowData = {};
            Array.from(row.cells).forEach((cell, index) => {
                const header = document.querySelector(`.annotation-table th:nth-child(${index + 1})`).textContent.trim();
                rowData[header] = cell.textContent.trim();
            });
            data.push(rowData);
        });

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });

        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `export.${format}`;

        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
    }

    function exportAnnotations() {
        const selectedFormats = [];
        const checkboxes = document.querySelectorAll('.formatSelection input[name="format"]:checked');
        checkboxes.forEach(checkbox => selectedFormats.push(checkbox.value));

        if (selectedFormats.length === 0) {
            alert('Please select at least one format for export.');
            return;
        }

        selectedFormats.forEach(format => {
            exportData(format);
        });
    }
});
