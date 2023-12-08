function performSearch() {
    const searchQuery = document.querySelector('.search-container input[type=text]').value;
    if (searchQuery.trim() !== '') {
        window.location.href = `videos.html?search=${encodeURIComponent(searchQuery)}`;
    }
}