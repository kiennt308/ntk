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
          <div style="margin-bottom: 0.75rem; color: var(--text-muted); display: flex; justify-content: center;">
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="M6 8h.001M10 8h.001M14 8h.001M18 8h.001M6 12h.001M18 12h.001M8 16h8"/></svg>
          </div>
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
          <div style="margin-bottom: 0.75rem; color: var(--text-muted); display: flex; justify-content: center;">
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </div>
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
            <div class="card__badges">
              <span class="badge badge--primary">${post.category || 'Guide'}</span>
            </div>
            <div class="card__meta">
              <span class="card__meta-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                <span>${post.date}</span>
              </span>
            </div>
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
