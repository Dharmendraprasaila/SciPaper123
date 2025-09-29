document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const ingestBtn = document.getElementById('ingest-btn');
    const searchBtn = document.getElementById('search-btn');
    const collabBtn = document.getElementById('collab-btn');

    const ingestQuery = document.getElementById('ingest-query');
    const ingestSource = document.getElementById('ingest-source');
    const searchQuery = document.getElementById('search-query');
    const collabQuery = document.getElementById('collab-query');

    const ingestStatus = document.getElementById('ingest-status');
    const searchResults = document.getElementById('search-results');
    const collabResults = document.getElementById('collab-results');
    const paperDetailsContainer = document.getElementById('paper-details-container');

    let papersData = []; // To store search results

    // --- API Helper ---
    async function apiFetch(url, options = {}) {
        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'An API error occurred');
            }
            return response.json();
        } catch (error) {
            console.error('API Fetch Error:', error);
            throw error;
        }
    }

    // --- Event Listeners ---
    ingestBtn.addEventListener('click', handleIngest);
    searchBtn.addEventListener('click', handleSearch);
    collabBtn.addEventListener('click', handleCollabSearch);

    // --- Handlers ---
    async function handleIngest() {
        const query = ingestQuery.value.trim();
        const source = ingestSource.value;
        if (!query) {
            ingestStatus.textContent = 'Please enter a topic to ingest.';
            return;
        }

        ingestStatus.textContent = `🔄 Ingesting papers on '${query}' from ${source}...`;
        try {
            const data = await apiFetch(`/api/v1/ingest/?query=${encodeURIComponent(query)}&source=${source}`, { method: 'POST' });
            ingestStatus.textContent = `✅ Successfully ingested ${data.length} paper(s).`;
        } catch (error) {
            ingestStatus.textContent = `❌ Error: ${error.message}`;
        }
    }

    async function handleSearch() {
        const query = searchQuery.value.trim();
        if (!query) {
            searchResults.innerHTML = '<p>Please enter a search query.</p>';
            return;
        }

        searchResults.innerHTML = '<p>🔍 Searching...</p>';
        try {
            papersData = await apiFetch(`/api/v1/search/?query=${encodeURIComponent(query)}`);
            renderSearchResults(papersData);
        } catch (error) {
            searchResults.innerHTML = `<p>❌ Error: ${error.message}</p>`;
        }
    }

    async function handleCollabSearch() {
        const query = collabQuery.value.trim();
        if (!query) {
            collabResults.innerHTML = '<p>Please enter a topic.</p>';
            return;
        }

        collabResults.innerHTML = '<p>🤝 Finding experts...</p>';
        try {
            const data = await apiFetch(`/api/v1/collaborators/?topic=${encodeURIComponent(query)}`);
            renderCollabResults(data);
        } catch (error) {
            collabResults.innerHTML = `<p>❌ Error: ${error.message}</p>`;
        }
    }

    async function handleAnalyze(paperId) {
        const container = document.getElementById('ai-analysis-results');
        container.innerHTML = '<p>🧠 Analyzing with AI...</p>';
        try {
            const data = await apiFetch(`/api/v1/analyze/${paperId}`, { method: 'POST' });
            renderAnalysisResults(data);
        } catch (error) {
            container.innerHTML = `<p>❌ AI Analysis Error: ${error.message}</p>`;
        }
    }

    // --- Render Functions ---
    function renderSearchResults(papers) {
        if (papers.length === 0) {
            searchResults.innerHTML = '<p>No results found.</p>';
            return;
        }
        const ul = document.createElement('ul');
        papers.forEach((paper, index) => {
            const li = document.createElement('li');
            li.textContent = paper.title;
            li.dataset.index = index;
            li.addEventListener('click', () => renderPaperDetails(papers[index]));
            ul.appendChild(li);
        });
        searchResults.innerHTML = '';
        searchResults.appendChild(ul);
    }

    function renderCollabResults(collaborators) {
        if (collaborators.length === 0) {
            collabResults.innerHTML = '<p>No potential collaborators found.</p>';
            return;
        }
        const ul = document.createElement('ul');
        collaborators.forEach(collab => {
            const li = document.createElement('li');
            li.textContent = `${collab.author} (${collab.papers} paper(s))`;
            ul.appendChild(li);
        });
        collabResults.innerHTML = '';
        collabResults.appendChild(ul);
    }

    function renderPaperDetails(paper) {
        paperDetailsContainer.innerHTML = `
            <h3>${paper.title}</h3>
            <p><strong>Authors:</strong> ${paper.authors ? paper.authors.map(a => a.name).join(', ') : 'N/A'}</p>
            <p><strong>Journal:</strong> ${paper.journal || 'N/A'} | <strong>Year:</strong> ${paper.year || 'N/A'}</p>
            <p><strong>Abstract:</strong> ${paper.abstract || 'N/A'}</p>
            <button id="analyze-btn" data-id="${paper.id}">Analyze with AI</button>
            <div id="ai-analysis-results"></div>
        `;
        document.getElementById('analyze-btn').addEventListener('click', (e) => handleAnalyze(e.target.dataset.id));
    }

    function renderAnalysisResults(analysis) {
        const container = document.getElementById('ai-analysis-results');
        container.innerHTML = `
            <div class="analysis-section">
                <h4>Key Findings</h4>
                <ul>${analysis.findings.map(f => `<li>${f}</li>`).join('')}</ul>
            </div>
            <div class="analysis-section">
                <h4>Methods Used</h4>
                <ul>${analysis.methods.map(m => `<li>${m}</li>`).join('')}</ul>
            </div>
            <div class="analysis-section">
                <h4>Research Gaps</h4>
                <ul>${analysis.gaps.map(g => `<li>${g}</li>`).join('')}</ul>
            </div>
        `;
    }
});
