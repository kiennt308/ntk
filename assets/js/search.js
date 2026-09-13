document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');

  if (!searchInput || !searchResults) return;

  let searchIndex = [];
  const searchUrl = searchInput.getAttribute('data-search-url') || '/search.json';
  const abortController = new AbortController();

  // Helper: Secure HTML escape to prevent XSS (BUG-11)
  function escapeHTML(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Helper: Debounce function for smooth typing (BUG-95)
  function debounce(fn, delay) {
    let timer = null;
    return function (...args) {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), delay);
    };
  }

  // Fetch search index JSON with abort controller (BUG-94)
  fetch(searchUrl, { signal: abortController.signal })
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => {
      searchIndex = Array.isArray(data) ? data : [];
      // Handle initial query parameter from URL (BUG-07)
      const params = new URLSearchParams(window.location.search);
      const rawQuery = params.get('q') || params.get('query');
      if (rawQuery) {
        const decodedQuery = decodeURIComponent(rawQuery).trim();
        searchInput.value = decodedQuery;
        performSearch(decodedQuery);
      }
    })
    .catch(err => {
      if (err.name !== 'AbortError') {
        console.error('Error fetching search index:', err);
        searchResults.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem 0;">Error loading search index. Please refresh the page.</p>';
      }
    });

  // Debounced typing handler
  const debouncedSearch = debounce((query) => {
    performSearch(query);
  }, 200);

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    debouncedSearch(query);
  });

  function performSearch(query) {
    if (!query) {
      searchResults.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem 0;">
          <div style="margin-bottom: 0.75rem; color: var(--text-muted); display: flex; justify-content: center;">
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="M6 8h.001M10 8h.001M14 8h.001M18 8h.001M6 12h.001M18 12h.001M8 16h8"/></svg>
          </div>
          <p>Start typing keywords to search the engineering documentation...</p>
        </div>
      `;
      return;
    }

    // Split and filter out empty strings (BUG-100)
    const keywords = query.toLowerCase().split(/\s+/).filter(Boolean);
    const matches = searchIndex.filter(post => {
      return keywords.every(kw => {
        const inTitle = (post.title || '').toLowerCase().includes(kw);
        const inDesc = (post.description || '').toLowerCase().includes(kw);
        const inContent = (post.content || '').toLowerCase().includes(kw);
        const inCategory = (post.category || '').toLowerCase().includes(kw);
        const inTags = (post.tags || []).some(tag => String(tag).toLowerCase().includes(kw));

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
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </div>
          <h3 style="margin: 0 0 0.5rem 0;">No matching articles found</h3>
          <p style="color: var(--text-secondary);">Try broader keywords or browse by topics on the home page.</p>
        </div>
      `;
      return;
    }

    searchResults.innerHTML = results.map(post => {
      const escapedTitle = escapeHTML(post.title);
      const escapedDesc = escapeHTML(post.description);
      const escapedCat = escapeHTML(post.category || 'Guide');
      const escapedDate = escapeHTML(post.date);
      const escapedUrl = escapeHTML(post.url);

      const tagsMarkup = Array.isArray(post.tags) && post.tags.length > 0
        ? post.tags.map(t => `<span class="badge">#${escapeHTML(t)}</span>`).join(' ')
        : '';
        
      return `
        <article class="card">
          <div class="card__top">
            <div class="card__badges">
              <span class="badge badge--primary">${escapedCat}</span>
            </div>
            <div class="card__meta">
              <span class="card__meta-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                <span>${escapedDate}</span>
              </span>
            </div>
          </div>
          <h3 class="card__title"><a href="${escapedUrl}">${escapedTitle}</a></h3>
          <p class="card__description">${escapedDesc}</p>
          <div class="card__tags">
            ${tagsMarkup}
          </div>
        </article>
      `;
    }).join('');
  }
});
