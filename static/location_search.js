document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById('location-search');
    const searchResults = document.getElementById('search-results');

    searchInput.addEventListener('input', async () => {
        const query = searchInput.value.toLowerCase();
        searchResults.innerHTML = '';
        if (query) {
            const response = await fetch(`/search?query=${query}`);
            const data = await response.json();
            const filteredLocations = data.places;
            filteredLocations.forEach(location => {
                const li = document.createElement('li');
                li.textContent = location;
                searchResults.appendChild(li);
            });
        }
    });

    searchResults.addEventListener('click', async (event) => {
        if (event.target.tagName === 'LI') {
            const placeName = event.target.textContent;
            const response = await fetch(`/coordinates?place=${placeName}`);
            const data = await response.json();
            alert(data.message);
        }
    });
});
