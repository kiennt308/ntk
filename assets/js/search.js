document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');

  if (!searchInput || !searchResults) return;

  let searchIndex = [];
  const searchUrl = searchInput.getAttribute('data-search-url') || '/search.json';

  // Fetch the search index JSON compiled by Jekyll
  fetch(searchUrl)
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
      searchResults.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted);">Error loading search index. Please refresh.</p>';
    });

  // Handle typing inputs
  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    performSearch(query);
  });

  function performSearch(query) {
    if (!query) {
      searchResults.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem 0;">
          <div style="font-size: 2rem; margin-bottom: 0.5rem;">⌨️</div>
          <p>Start typing keywords to search the engineering documentation...</p>
        </div>
      `;
      return;
    }

    const keywords = query.toLowerCase().split(/\s+/);
    const matches = searchIndex.filter(post => {
      return keywords.every(kw => {
        const inTitle = (post.title || '').toLowerCase().includes(kw);
        const inDesc = (post.description || '').toLowerCase().includes(kw);
        const inContent = (post.content || '').toLowerCase().includes(kw);
        const inCategory = (post.category || '').toLowerCase().includes(kw);
        const inTags = (post.tags || []).some(tag => tag.toLowerCase().includes(kw));

        return inTitle || inDesc || inContent || inCategory || inTags;
      });
    });

    renderResults(matches);
  }

  function renderResults(results) {
    if (results.length === 0) {
      searchResults.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 4rem 1rem; background: var(--bg-surface); border: 1px dashed var(--border-color); border-radius: var(--radius-lg);">
          <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
          <h3 style="margin: 0 0 0.5rem 0;">No matching articles found</h3>
          <p style="color: var(--text-secondary);">Try broader keywords or browse by topics on the home page.</p>
        </div>
      `;
      return;
    }

    searchResults.innerHTML = results.map(post => {
      const tagsMarkup = post.tags && post.tags.length > 0
        ? post.tags.map(t => `<span class="badge">#${t}</span>`).join(' ')
        : '';
        
      return `
        <article class="card">
          <div class="card__top">
            <span class="badge badge--primary">${post.category || 'Guide'}</span>
            <span style="font-size: 0.8rem; color: var(--text-muted);">${post.date}</span>
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
