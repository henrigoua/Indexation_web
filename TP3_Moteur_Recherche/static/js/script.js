function search() {
    let query = document.getElementById("searchQuery").value;
    let searchType = document.getElementById("searchType").value;
    let topK = document.getElementById("topK").value;
    let resultsDiv = document.getElementById("results");

    resultsDiv.innerHTML = "<p>Searching...</p>"; 

    fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query, search_type: searchType, top_k: parseInt(topK) })
    })
    .then(response => response.json())
    .then(data => {
        resultsDiv.innerHTML = "";

        if (data.results.length === 0) {
            resultsDiv.innerHTML = "<p>No results found.</p>"; 
        } else {
            data.results.forEach(item => {
                resultsDiv.innerHTML += `
                    <div class="result-item">
                        <img src="${item.image || 'default-image.png'}" alt="${item.title}" class="product-image">
                        <div class="product-info">
                            <strong>${item.title}</strong><br>
                            <p><strong>Origin:</strong> ${item.features.made_in || 'Not specified'}</p> <!-- Updated -->
                            <p><strong>Score:</strong> ${item.score || 'Not available'}</p> <!-- Updated -->
                            <p>${item.description || 'Description not available'}</p> <!-- Updated -->
                            <a href="${item.url}" target="_blank" class="product-link">Learn more</a> <!-- Updated -->
                        </div>
                    </div>
                `;
            });
        }
    })
    .catch(error => {
        resultsDiv.innerHTML = "<p>Error during search.</p>"; 
        console.error(error);
    });
}
