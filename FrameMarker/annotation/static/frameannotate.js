document.addEventListener('DOMContentLoaded', function () {
    const frameImage = document.querySelector('.selected-frame');
    const rankButtons = document.querySelectorAll('.rank-btn');
    const annotateButton = document.getElementById('annotateBtn');
    const choosedRankElement = document.getElementById('choosed-rank');
    const recordedElement = document.getElementById('rank-info');

    let selectedRank = null;

    // Event listener for rank buttons
    rankButtons.forEach((btn) => {
        btn.addEventListener('click', function () {
            // Highlight the selected rank button
            rankButtons.forEach((button) => {
                button.classList.remove('selected');
            });
            btn.classList.add('selected');

            // Store the selected rank
            selectedRank = btn.dataset.rank;
        });
    });

    // Event listener for annotate button
    annotateButton.addEventListener('click', function () {
        if (selectedRank !== null) {
            // Display the selected rank in the chosen rank section
            choosedRankElement.textContent = selectedRank;

            // Show the "Recorded" message
            recordedElement.style.display = 'block';

            // Disable the annotate button after annotation
            annotateButton.disabled = true;

            // You can add additional UI updates or messages here if needed

            // Optionally, you can submit a form for server-side processing
            // document.forms["annotationForm"].submit();
        }
    });
});
