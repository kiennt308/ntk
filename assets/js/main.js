document.addEventListener('DOMContentLoaded', () => {
  /* ==========================================================================
     1. Toast Notification Utility (Debounced & Race-Condition Safe: BUG-01)
     ========================================================================== */
  let toastTimer = null;
  function showToast(message) {
    let toast = document.getElementById('toast-notification');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'toast-notification';
      toast.setAttribute('aria-live', 'polite');
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');

    if (toastTimer) {
      clearTimeout(toastTimer);
    }

    toastTimer = setTimeout(() => {
      toast.classList.remove('show');
      toastTimer = null;
    }, 2500);
  }

  /* ==========================================================================
     2. Resilient Clipboard Copy Helper (HTTPS + Fallback: BUG-02)
     ========================================================================== */
  function copyTextToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    } else {
      // Fallback using temporary textarea
      return new Promise((resolve, reject) => {
        try {
          const textArea = document.createElement('textarea');
          textArea.value = text;
          textArea.style.position = 'fixed';
          textArea.style.left = '-999999px';
          textArea.style.top = '-999999px';
          document.body.appendChild(textArea);
          textArea.focus();
          textArea.select();
          const successful = document.execCommand('copy');
          document.body.removeChild(textArea);
          if (successful) {
            resolve();
          } else {
            reject(new Error('execCommand copy unsuccessful'));
          }
        } catch (err) {
          reject(err);
        }
      });
    }
  }

  /* ==========================================================================
     3. Debounce Utility (BUG-95)
     ========================================================================== */
  function debounce(fn, delay) {
    let timer = null;
    return function (...args) {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), delay);
    };
  }

  /* ==========================================================================
     4. Dark Mode Toggle Logic (Safe Storage & ARIA Sync: BUG-96)
     ========================================================================== */
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const isDark = document.documentElement.classList.toggle('dark-theme');
      try {
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
      } catch (e) {
        // Handle QuotaExceeded or Incognito mode restrictions gracefully
      }
      themeToggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    });
  }

  /* ==========================================================================
     5. Mobile Hamburger Menu (Backdrop, Focus Trap & ARIA: BUG-58, BUG-141, BUG-185)
     ========================================================================== */
  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.querySelector('.nav-menu');

  if (hamburger && navMenu) {
    let backdrop = document.querySelector('.nav-backdrop');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.className = 'nav-backdrop';
      document.body.appendChild(backdrop);
    }

    function toggleMenu(openState) {
      const isOpen = openState !== undefined ? openState : !navMenu.classList.contains('open');
      hamburger.classList.toggle('open', isOpen);
      navMenu.classList.toggle('open', isOpen);
      backdrop.classList.toggle('open', isOpen);
      hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      document.body.style.overflow = isOpen ? 'hidden' : '';

      if (isOpen) {
        const firstLink = navMenu.querySelector('a');
        if (firstLink) firstLink.focus();
      }
    }

    hamburger.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleMenu();
    });

    backdrop.addEventListener('click', () => {
      toggleMenu(false);
    });

    // Close mobile menu when clicking outside safely
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.hamburger') && !e.target.closest('.nav-menu')) {
        toggleMenu(false);
      }
    });

    // Close menu when clicking navigation links
    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        toggleMenu(false);
      });
    });

    // Keyboard focus trap inside mobile nav
    navMenu.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        toggleMenu(false);
        hamburger.focus();
      }
    });
  }

  /* ==========================================================================
     6. Throttled Scroll Engine: Reading Progress & Header Shadow (BUG-03, BUG-05)
     ========================================================================== */
  const progressBar = document.getElementById('reading-progress');
  const header = document.querySelector('header.navbar');
  const articleMain = document.querySelector('.article-main');
  const backToTopBtn = document.getElementById('back-to-top');

  let isScrollScheduled = false;

  function onScrollFrame() {
    const scrollY = window.pageYOffset || document.documentElement.scrollTop;

    // Header shadow on scroll
    if (header) {
      if (scrollY > 15) {
        header.style.boxShadow = 'var(--shadow-md)';
      } else {
        header.style.boxShadow = 'none';
      }
    }

    // Article reading progress calculation (Division-by-zero protected: BUG-03)
    if (progressBar && articleMain) {
      const articleTop = articleMain.offsetTop;
      const articleHeight = articleMain.offsetHeight;
      const windowHeight = window.innerHeight;
      const denominator = Math.max(1, articleHeight - windowHeight * 0.4);

      const progress = Math.min(
        100,
        Math.max(0, ((scrollY - articleTop + windowHeight * 0.4) / denominator) * 100)
      );
      progressBar.style.width = `${progress}%`;
    }

    // Back to top floating button
    if (backToTopBtn) {
      if (scrollY > 300) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    }

    isScrollScheduled = false;
  }

  window.addEventListener('scroll', () => {
    if (!isScrollScheduled) {
      isScrollScheduled = true;
      window.requestAnimationFrame(onScrollFrame);
    }
  }, { passive: true });

  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  /* ==========================================================================
     7. Kramdown Code Block Headers & Copy Functionality (BUG-02, BUG-10)
     ========================================================================== */
  const languageAliases = {
    'BASH': 'BASH',
    'SH': 'SHELL',
    'ZSH': 'ZSH',
    'YML': 'YAML',
    'YAML': 'YAML',
    'JSON': 'JSON',
    'TERRAFORM': 'TERRAFORM',
    'TF': 'TERRAFORM',
    'DOCKERFILE': 'DOCKER',
    'KUBERNETES': 'K8S',
    'K8S': 'K8S',
    'GO': 'GOLANG',
    'PYTHON': 'PYTHON',
    'PY': 'PYTHON',
    'TEXT': 'TXT'
  };

  const codeBlocks = document.querySelectorAll('div.highlighter-rouge, figure.highlight');
  
  codeBlocks.forEach(wrapper => {
    let rawLang = 'CODE';
    wrapper.classList.forEach(cls => {
      if (cls.startsWith('language-')) {
        rawLang = cls.replace('language-', '').toUpperCase();
      }
    });

    const displayLang = languageAliases[rawLang] || rawLang;

    let headerEl = wrapper.querySelector('.code-header');
    if (!headerEl) {
      headerEl = document.createElement('div');
      headerEl.className = 'code-header';
      
      const leftCol = document.createElement('div');
      leftCol.style.display = 'flex';
      leftCol.style.alignItems = 'center';
      leftCol.style.gap = '8px';

      const dots = document.createElement('div');
      dots.className = 'code-header-dots';
      dots.innerHTML = '<span class="code-header-dot"></span><span class="code-header-dot"></span><span class="code-header-dot"></span>';

      const langSpan = document.createElement('span');
      langSpan.className = 'code-header-lang';
      langSpan.textContent = displayLang;

      leftCol.appendChild(dots);
      leftCol.appendChild(langSpan);
      headerEl.appendChild(leftCol);

      const copyBtn = document.createElement('button');
      copyBtn.className = 'btn-copy';
      copyBtn.type = 'button';
      copyBtn.setAttribute('aria-label', `Copy ${displayLang} code`);
      copyBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
        <span>Copy</span>
      `;
      
      copyBtn.addEventListener('click', () => {
        const code = wrapper.querySelector('pre code') || wrapper.querySelector('pre');
        if (code) {
          let rawText = code.innerText;
          // Strip bash prompt ($ or #) when copying commands (BUG-202)
          if (['BASH', 'SHELL', 'ZSH'].includes(displayLang)) {
            rawText = rawText.split('\n').map(line => line.replace(/^[$#]\s+/, '')).join('\n');
          }
          copyTextToClipboard(rawText).then(() => {
            copyBtn.querySelector('span').textContent = 'Copied!';
            copyBtn.style.color = '#34d399';
            showToast('Code snippet copied to clipboard!');
            setTimeout(() => {
              copyBtn.querySelector('span').textContent = 'Copy';
              copyBtn.style.color = '';
            }, 2000);
          }).catch(err => {
            console.error('Copy failed: ', err);
            copyBtn.querySelector('span').textContent = 'Error';
          });
        }
      });

      headerEl.appendChild(copyBtn);
      wrapper.insertBefore(headerEl, wrapper.firstChild);
    }

    // Code Block Collapse for long snippets (> 35 lines) (BUG-203)
    const preEl = wrapper.querySelector('pre');
    if (preEl && preEl.innerText.split('\n').length > 35) {
      wrapper.classList.add('code-collapsed');
      const expandBtn = document.createElement('div');
      expandBtn.className = 'code-expand-btn';
      expandBtn.innerHTML = '<button class="btn btn--secondary btn--sm" type="button" style="font-size:0.8rem; padding:0.35rem 0.85rem;">Expand Code ▾</button>';
      expandBtn.querySelector('button').addEventListener('click', () => {
        wrapper.classList.remove('code-collapsed');
        expandBtn.remove();
      });
      wrapper.appendChild(expandBtn);
    }
  });

  /* ==========================================================================
     8. Copy Page URL / Share Button (BUG-02)
     ========================================================================== */
  const copyLinkButtons = document.querySelectorAll('.btn-copy-link');
  copyLinkButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const url = window.location.href;
      copyTextToClipboard(url).then(() => {
        showToast('Article link copied to clipboard!');
      }).catch(() => {
        showToast('Failed to copy link.');
      });
    });
  });

  /* ==========================================================================
     9. Live Blog Category Filtering, Instant Search & Pagination (BUG-04, BUG-08, BUG-09, BUG-95)
     ========================================================================== */
  const filterButtons = document.querySelectorAll('.live-filter-btn');
  const postCards = Array.from(document.querySelectorAll('.post-card-item'));
  const blogSearchInput = document.getElementById('blog-live-search');
  const postCountDisplay = document.getElementById('visible-post-count');
  const paginationWrapper = document.getElementById('blog-pagination');
  const paginationControls = document.getElementById('pagination-controls');
  const postsGrid = document.getElementById('posts-grid');

  if (postCards.length > 0) {
    const POSTS_PER_PAGE = 8;
    let currentCategory = 'all';
    let searchQuery = '';
    let currentPage = 1;
    let matchingCards = [];

    function scrollToGrid() {
      if (postsGrid) {
        const yOffset = -90;
        const y = postsGrid.getBoundingClientRect().top + window.pageYOffset + yOffset;
        window.scrollTo({ top: y, behavior: 'smooth' });
      }
    }

    function renderPagination() {
      const totalPosts = matchingCards.length;

      // Handle empty filtered posts (BUG-08)
      if (totalPosts === 0) {
        postCards.forEach(card => { card.style.display = 'none'; });
        if (postCountDisplay) postCountDisplay.textContent = '0';
        const emptyNotice = document.getElementById('no-filter-results');
        if (emptyNotice) emptyNotice.style.display = 'block';
        if (paginationWrapper) paginationWrapper.style.display = 'none';
        return;
      }

      const totalPages = Math.ceil(totalPosts / POSTS_PER_PAGE) || 1;

      if (currentPage > totalPages) {
        currentPage = 1;
      }

      // Hide all cards first
      postCards.forEach(card => {
        card.style.display = 'none';
      });

      // Show cards for the current page
      const startIndex = (currentPage - 1) * POSTS_PER_PAGE;
      const endIndex = startIndex + POSTS_PER_PAGE;
      const pageCards = matchingCards.slice(startIndex, endIndex);

      pageCards.forEach(card => {
        card.style.display = 'flex';
      });

      if (postCountDisplay) {
        postCountDisplay.textContent = totalPosts;
      }

      const emptyNotice = document.getElementById('no-filter-results');
      if (emptyNotice) {
        emptyNotice.style.display = 'none';
      }

      if (!paginationWrapper || !paginationControls) return;

      if (totalPosts <= POSTS_PER_PAGE) {
        paginationWrapper.style.display = 'none';
        return;
      }

      paginationWrapper.style.display = 'flex';
      paginationControls.innerHTML = '';

      // Previous Page Button
      const prevBtn = document.createElement('button');
      prevBtn.className = `page-btn ${currentPage === 1 ? 'disabled' : ''}`;
      prevBtn.innerHTML = '‹ Prev';
      prevBtn.type = 'button';
      prevBtn.setAttribute('aria-label', 'Previous Page');
      prevBtn.addEventListener('click', () => {
        if (currentPage > 1) {
          currentPage--;
          renderPagination();
          scrollToGrid();
        }
      });
      paginationControls.appendChild(prevBtn);

      // Page Number Buttons with Smart Sliding Window & Ellipsis
      function getPaginationRange(current, total) {
        if (total <= 7) {
          return Array.from({ length: total }, (_, i) => i + 1);
        }

        if (current <= 4) {
          return [1, 2, 3, 4, 5, '...', total];
        }

        if (current >= total - 3) {
          return [1, '...', total - 4, total - 3, total - 2, total - 1, total];
        }

        return [1, '...', current - 1, current, current + 1, '...', total];
      }

      const pageRange = getPaginationRange(currentPage, totalPages);

      pageRange.forEach((item) => {
        if (item === '...') {
          const ellipsis = document.createElement('span');
          ellipsis.className = 'pagination-ellipsis';
          ellipsis.textContent = '…';
          ellipsis.setAttribute('aria-hidden', 'true');
          paginationControls.appendChild(ellipsis);
        } else {
          const pageBtn = document.createElement('button');
          pageBtn.className = `page-btn ${item === currentPage ? 'active' : ''}`;
          pageBtn.textContent = item;
          pageBtn.type = 'button';
          pageBtn.setAttribute('aria-label', `Page ${item}`);
          if (item === currentPage) {
            pageBtn.setAttribute('aria-current', 'page');
          }
          pageBtn.addEventListener('click', () => {
            if (currentPage !== item) {
              currentPage = item;
              renderPagination();
              scrollToGrid();
            }
          });
          paginationControls.appendChild(pageBtn);
        }
      });

      // Next Page Button
      const nextBtn = document.createElement('button');
      nextBtn.className = `page-btn ${currentPage === totalPages ? 'disabled' : ''}`;
      nextBtn.innerHTML = 'Next ›';
      nextBtn.type = 'button';
      nextBtn.setAttribute('aria-label', 'Next Page');
      nextBtn.addEventListener('click', () => {
        if (currentPage < totalPages) {
          currentPage++;
          renderPagination();
          scrollToGrid();
        }
      });
      paginationControls.appendChild(nextBtn);
    }

    function updateFilteredPosts() {
      matchingCards = postCards.filter(card => {
        const categoriesRaw = (card.getAttribute('data-categories') || '').toLowerCase();
        const categoriesList = categoriesRaw.split(/\s+/).filter(Boolean);
        const tags = (card.getAttribute('data-tags') || '').toLowerCase();
        const title = (card.getAttribute('data-title') || '').toLowerCase();
        const desc = (card.getAttribute('data-desc') || '').toLowerCase();

        // Exact category matching to avoid substring collisions (BUG-04)
        const matchesCategory = currentCategory === 'all' || categoriesList.includes(currentCategory);
        const matchesSearch = !searchQuery || 
          title.includes(searchQuery) || 
          desc.includes(searchQuery) || 
          tags.includes(searchQuery) || 
          categoriesRaw.includes(searchQuery);

        return matchesCategory && matchesSearch;
      });

      currentPage = 1;
      renderPagination();
    }

    filterButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentCategory = (btn.getAttribute('data-filter') || 'all').toLowerCase();
        updateFilteredPosts();
      });
    });

    if (blogSearchInput) {
      const debouncedBlogSearch = debounce((query) => {
        searchQuery = query;
        updateFilteredPosts();
      }, 200);

      blogSearchInput.addEventListener('input', (e) => {
        debouncedBlogSearch(e.target.value.trim().toLowerCase());
      });
    }

    // Sidebar filter triggers
    const sidebarTriggers = document.querySelectorAll('.sidebar-filter-trigger');
    sidebarTriggers.forEach(trigger => {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        const filterVal = (trigger.getAttribute('data-filter') || '').toLowerCase();
        const targetBtn = Array.from(filterButtons).find(b => (b.getAttribute('data-filter') || '').toLowerCase() === filterVal);
        if (targetBtn) {
          targetBtn.click();
          scrollToGrid();
        }
      });
    });

    // Check URL hash for initial filter with decodeURIComponent (BUG-09)
    if (window.location.hash) {
      try {
        const hash = decodeURIComponent(window.location.hash.replace('#', '')).toLowerCase();
        const targetBtn = Array.from(filterButtons).find(b => (b.getAttribute('data-filter') || '').toLowerCase() === hash);
        if (targetBtn) {
          targetBtn.click();
        } else {
          updateFilteredPosts();
        }
      } catch (e) {
        updateFilteredPosts();
      }
    } else {
      updateFilteredPosts();
    }
  }

  /* ==========================================================================
     10. Technical Diagram Image Lightbox Zoom (BUG-193)
     ========================================================================== */
  const articleImages = document.querySelectorAll('.article-body img');
  if (articleImages.length > 0) {
    let lightboxOverlay = document.getElementById('lightbox-overlay');
    if (!lightboxOverlay) {
      lightboxOverlay = document.createElement('div');
      lightboxOverlay.id = 'lightbox-overlay';
      lightboxOverlay.className = 'lightbox-overlay';
      lightboxOverlay.setAttribute('role', 'dialog');
      lightboxOverlay.setAttribute('aria-modal', 'true');
      lightboxOverlay.setAttribute('aria-label', 'Image preview');
      lightboxOverlay.innerHTML = '<img class="lightbox-img" src="" alt="Enlarged architecture diagram" />';
      document.body.appendChild(lightboxOverlay);
    }
    const lightboxImg = lightboxOverlay.querySelector('.lightbox-img');

    articleImages.forEach(img => {
      img.addEventListener('click', () => {
        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt || 'Enlarged technical diagram';
        lightboxOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
      });
    });

    lightboxOverlay.addEventListener('click', () => {
      lightboxOverlay.classList.remove('active');
      document.body.style.overflow = '';
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lightboxOverlay.classList.contains('active')) {
        lightboxOverlay.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  }

  /* ==========================================================================
     11. Native Web Share API Support (BUG-198)
     ========================================================================== */
  const nativeShareButtons = document.querySelectorAll('.btn-native-share');
  nativeShareButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (navigator.share) {
        e.preventDefault();
        navigator.share({
          title: document.title,
          url: window.location.href
        }).catch(() => {});
      }
    });
  });

  /* ==========================================================================
     12. Global Keyboard Shortcut for Search (Ctrl+K / Cmd+K: BUG-215, BUG-232)
     ========================================================================== */
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      const searchInput = document.getElementById('search-input') || document.getElementById('blog-live-search');
      if (searchInput) {
        searchInput.focus();
        searchInput.select();
      } else {
        const searchLink = document.querySelector('a[href*="search"]');
        if (searchLink) searchLink.click();
      }
    }
  });

  /* ==========================================================================
     13. Copy Email Address Quick Action (BUG-234)
     ========================================================================== */
  const copyEmailButtons = document.querySelectorAll('.btn-copy-email');
  copyEmailButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const email = btn.getAttribute('data-email') || 'kiennt.sg@gmail.com';
      copyTextToClipboard(email).then(() => {
        showToast(`Email copied: ${email}`);
      }).catch(() => {
        window.location.href = `mailto:${email}`;
      });
    });
  });

  /* ==========================================================================
     14. Network Offline / Online Toast Indicator for PWA (BUG-297)
     ========================================================================== */
  window.addEventListener('offline', () => {
    showToast('You are currently offline. Cached articles remain accessible.');
  });
  window.addEventListener('online', () => {
    showToast('Internet connection restored.');
  });

  /* ==========================================================================
     15. Mermaid Diagram Auto-Renderer & Interactive Zoom Lightbox
     ========================================================================== */
  function initMermaidDiagrams() {
    if (typeof mermaid === 'undefined') return;

    const mermaidCodes = document.querySelectorAll(
      'code.language-mermaid, pre.language-mermaid, div.language-mermaid pre code, .highlighter-rouge.language-mermaid pre code, .language-mermaid pre'
    );

    if (mermaidCodes.length > 0) {
      mermaidCodes.forEach((codeEl) => {
        const rawContent = codeEl.textContent || codeEl.innerText;
        const container = codeEl.closest('.highlighter-rouge') || codeEl.closest('pre') || codeEl;

        const mermaidWrapper = document.createElement('div');
        mermaidWrapper.className = 'mermaid-wrapper';

        const mermaidInner = document.createElement('div');
        mermaidInner.className = 'mermaid';
        mermaidInner.textContent = rawContent.trim();

        const zoomHint = document.createElement('button');
        zoomHint.className = 'mermaid-zoom-btn';
        zoomHint.type = 'button';
        zoomHint.setAttribute('aria-label', 'Phóng to sơ đồ');
        zoomHint.title = 'Bấm để phóng to và tương tác với sơ đồ';
        zoomHint.innerHTML = '<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg><span>Phóng to</span>';

        mermaidWrapper.appendChild(mermaidInner);
        mermaidWrapper.appendChild(zoomHint);

        if (container && container.parentNode) {
          container.parentNode.replaceChild(mermaidWrapper, container);
        }
      });

      const isDark = document.documentElement.classList.contains('dark-theme');
      mermaid.initialize({
        startOnLoad: false,
        theme: isDark ? 'dark' : 'default',
        themeVariables: {
          darkMode: isDark,
          fontFamily: 'Inter, system-ui, -apple-system, sans-serif'
        },
        securityLevel: 'loose'
      });

      try {
        mermaid.run().then(() => {
          attachMermaidLightbox();
        });
      } catch (err) {
        console.warn('Mermaid rendering notice:', err);
      }
    } else {
      // If already rendered (e.g. static div.mermaid)
      attachMermaidLightbox();
    }
  }

  // Lightbox implementation with Zoom, Pan, Mousewheel, and Keyboard controls
  function attachMermaidLightbox() {
    let lightbox = document.getElementById('mermaid-lightbox');
    if (!lightbox) {
      lightbox = document.createElement('div');
      lightbox.id = 'mermaid-lightbox';
      lightbox.className = 'mermaid-lightbox';
      lightbox.setAttribute('aria-hidden', 'true');
      lightbox.innerHTML = `
        <div class="mermaid-lightbox-backdrop"></div>
        <div class="mermaid-lightbox-container" role="dialog" aria-label="Sơ đồ tương tác">
          <div class="mermaid-lightbox-toolbar">
            <span class="mermaid-lightbox-title">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
              <span>Interactive Architecture Viewer</span>
            </span>
            <div class="mermaid-lightbox-actions">
              <button type="button" class="lightbox-btn" id="lightbox-zoom-out" title="Thu nhỏ (Ctrl + -)" aria-label="Zoom out">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
              </button>
              <span class="lightbox-zoom-level" id="lightbox-zoom-level">100%</span>
              <button type="button" class="lightbox-btn" id="lightbox-zoom-in" title="Phóng to (Ctrl + +)" aria-label="Zoom in">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
              </button>
              <button type="button" class="lightbox-btn" id="lightbox-reset" title="Đặt lại kích thước (100%)" aria-label="Reset zoom">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path></svg>
              </button>
              <button type="button" class="lightbox-btn lightbox-btn--close" id="lightbox-close" title="Đóng (ESC)" aria-label="Close">
                <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              </button>
            </div>
          </div>
          <div class="mermaid-lightbox-viewport" id="mermaid-lightbox-viewport">
            <div class="mermaid-lightbox-content" id="mermaid-lightbox-content"></div>
          </div>
          <div class="mermaid-lightbox-hint">
            <span>🖱️ Kéo chuột để di chuyển (Pan)</span>
            <span class="hint-dot">•</span>
            <span>🔍 Cuộn chuột để phóng to / thu nhỏ</span>
            <span class="hint-dot">•</span>
            <span>⌨️ Nhấn ESC để đóng</span>
          </div>
        </div>
      `;
      document.body.appendChild(lightbox);

      let scale = 1;
      let panX = 0;
      let panY = 0;
      let isDragging = false;
      let startX = 0;
      let startY = 0;

      const content = document.getElementById('mermaid-lightbox-content');
      const viewport = document.getElementById('mermaid-lightbox-viewport');
      const zoomLevelDisplay = document.getElementById('lightbox-zoom-level');
      const backdrop = lightbox.querySelector('.mermaid-lightbox-backdrop');
      const closeBtn = document.getElementById('lightbox-close');
      const zoomInBtn = document.getElementById('lightbox-zoom-in');
      const zoomOutBtn = document.getElementById('lightbox-zoom-out');
      const resetBtn = document.getElementById('lightbox-reset');

      function updateTransform() {
        if (!content) return;
        content.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`;
        if (zoomLevelDisplay) {
          zoomLevelDisplay.textContent = `${Math.round(scale * 100)}%`;
        }
      }

      function openModal(svgElement) {
        if (!svgElement) return;
        content.innerHTML = '';
        const clonedSvg = svgElement.cloneNode(true);
        clonedSvg.style.maxWidth = 'none';
        clonedSvg.style.width = 'auto';
        clonedSvg.style.height = 'auto';
        content.appendChild(clonedSvg);

        scale = 1.25;
        panX = 0;
        panY = 0;
        updateTransform();

        lightbox.classList.add('active');
        lightbox.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
      }

      function closeModal() {
        lightbox.classList.remove('active');
        lightbox.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      }

      backdrop.addEventListener('click', closeModal);
      closeBtn.addEventListener('click', closeModal);

      document.addEventListener('keydown', (e) => {
        if (lightbox.classList.contains('active')) {
          if (e.key === 'Escape') closeModal();
          if (e.key === '+' || e.key === '=') {
            scale = Math.min(5, scale + 0.25);
            updateTransform();
          }
          if (e.key === '-' || e.key === '_') {
            scale = Math.max(0.4, scale - 0.25);
            updateTransform();
          }
          if (e.key === '0') {
            scale = 1;
            panX = 0;
            panY = 0;
            updateTransform();
          }
        }
      });

      zoomInBtn.addEventListener('click', () => {
        scale = Math.min(5, scale + 0.25);
        updateTransform();
      });

      zoomOutBtn.addEventListener('click', () => {
        scale = Math.max(0.4, scale - 0.25);
        updateTransform();
      });

      resetBtn.addEventListener('click', () => {
        scale = 1;
        panX = 0;
        panY = 0;
        updateTransform();
      });

      // Mousewheel Zoom
      viewport.addEventListener('wheel', (e) => {
        e.preventDefault();
        const delta = e.deltaY > 0 ? -0.15 : 0.15;
        scale = Math.min(5, Math.max(0.4, scale + delta));
        updateTransform();
      }, { passive: false });

      // Drag / Pan Interaction
      viewport.addEventListener('mousedown', (e) => {
        if (e.button !== 0) return;
        isDragging = true;
        startX = e.clientX - panX;
        startY = e.clientY - panY;
        viewport.classList.add('dragging');
      });

      window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        panX = e.clientX - startX;
        panY = e.clientY - startY;
        updateTransform();
      });

      window.addEventListener('mouseup', () => {
        if (isDragging) {
          isDragging = false;
          viewport.classList.remove('dragging');
        }
      });

      window._openMermaidLightbox = openModal;
    }

    const wrappers = document.querySelectorAll('.mermaid-wrapper, .mermaid');
    wrappers.forEach((box) => {
      const svg = box.querySelector('svg');
      if (svg) {
        box.style.cursor = 'zoom-in';
        box.onclick = (e) => {
          if (window._openMermaidLightbox) {
            window._openMermaidLightbox(svg);
          }
        };
      }
    });
  }

  // Initial render
  initMermaidDiagrams();

  // Re-initialize MathJax if needed on dynamic changes
  if (window.MathJax && window.MathJax.typesetPromise) {
    window.MathJax.typesetPromise().catch((err) => console.warn('MathJax typesetting error:', err));
  }
});
