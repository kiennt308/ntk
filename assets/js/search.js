document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');

  if (!searchInput || !searchResults) return;

  let searchIndex = [];

  // Fetch the search index JSON compiled by Jekyll
  fetch('/search.json')
    .then(response => response.json())
    .then(data => {
      searchIndex = data;
      // If there's an initial query parameter in the URL, populate and run search
      const params = new URLSearchParams(window.location.search);
      const query = params.get('q') || params.get('query');
      if (query) {
        searchInput.value = query;
        performSearch(query);
      }
    })
    .catch(err => {
      console.error('Error fetching search index:', err);
      searchResults.innerHTML = '<p class="text-center" style="grid-column: 1/-1;">Error loading search index. Please refresh.</p>';
    });

  // Handle typing inputs
  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    performSearch(query);
  });

  function performSearch(query) {
    if (!query) {
      // If query is empty, show all posts or empty depending on context
      // On search page we can show a prompt, on blog page we show all.
      const isSearchPage = window.location.pathname.includes('/search');
      if (isSearchPage) {
        searchResults.innerHTML = '<p class="text-center" style="grid-column: 1/-1; color: var(--text-muted);">Start typing to search articles...</p>';
      } else {
        renderResults(searchIndex);
      }
      return;
    }

    const keywords = query.toLowerCase().split(/\s+/);
    const matches = searchIndex.filter(post => {
      return keywords.every(kw => {
        const inTitle = post.title.toLowerCase().includes(kw);
        const inDesc = post.description.toLowerCase().includes(kw);
        const inContent = post.content.toLowerCase().includes(kw);
        const inCategory = post.category.toLowerCase().includes(kw);
        const inTags = post.tags.some(tag => tag.toLowerCase().includes(kw));

        return inTitle || inDesc || inContent || inCategory || inTags;
      });
    });

    renderResults(matches);
  }

  function renderResults(results) {
    if (results.length === 0) {
      searchResults.innerHTML = '<p class="text-center" style="grid-column: 1/-1; color: var(--text-muted); padding: 3rem 0;">No articles match your search criteria.</p>';
      return;
    }

    searchResults.innerHTML = results.map(post => {
      const tagsMarkup = post.tags && post.tags.length > 0
        ? post.tags.map(t => `<a href="/tags.html#${t.toLowerCase()}" class="badge">${t}</a>`).join(' ')
        : '';
        
      return `
        <article class="card">
          <div class="card__meta">
            <span class="badge badge--accent">${post.category}</span>
            <span>•</span>
            <span>${post.date}</span>
          </div>
          <h3 class="card__title"><a href="${post.url}">${post.title}</a></h3>
          <p class="card__description">${post.description}</p>
          <div class="card__tags">
            ${tagsMarkup}
          </div>
        </article>
      `;
    }).join('');
  }
});
