document.getElementById('ingest-btn').addEventListener('click', async () => {
    const query = document.getElementById('query').value;
    const source = document.getElementById('source').value;
    const resultsContainer = document.getElementById('results-container');

    if (!query) {
        resultsContainer.innerHTML = '<p>Please enter a query.</p>';
        return;
    }

    resultsContainer.innerHTML = '<p>Ingesting papers...</p>';

    try {
        const response = await fetch(`/api/v1/ingest/?query=${query}&source=${source}`, {
            method: 'POST',
        });

        if (!response.ok) {
            throw new Error('Failed to ingest papers');
        }

        const papers = await response.json();
        let html = '<h2>Ingested Papers</h2><ul>';
        papers.forEach(paper => {
            html += `<li>${paper.title}</li>`;
        });
        html += '</ul>';
        resultsContainer.innerHTML = html;
    } catch (error) {
        resultsContainer.innerHTML = `<p>Error: ${error.message}</p>`;
    }
});
