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

      // Default: Wrap is enabled
      wrapper.classList.add('code-wrapped');

      const actions = document.createElement('div');
      actions.className = 'code-header-actions';

      // 1. Wrap Toggle Button (Default: Active)
      const wrapBtn = document.createElement('button');
      wrapBtn.className = 'btn-code-action btn-wrap active';
      wrapBtn.type = 'button';
      wrapBtn.setAttribute('aria-label', 'Bật / Tắt tự động xuống dòng (Toggle Word Wrap)');
      wrapBtn.setAttribute('title', 'Tự động xuống dòng: ĐANG BẬT (Bấm để tắt)');
      wrapBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h10a3 3 0 013 3v0a3 3 0 01-3 3H11m0 0l2-2m-2 2l2 2M4 18h4" />
        </svg>
        <span>Wrap</span>
      `;

      wrapBtn.addEventListener('click', () => {
        const isWrapped = wrapper.classList.toggle('code-wrapped');
        wrapBtn.classList.toggle('active', isWrapped);
        if (isWrapped) {
          wrapBtn.setAttribute('title', 'Tự động xuống dòng: ĐANG BẬT (Bấm để tắt)');
        } else {
          wrapBtn.setAttribute('title', 'Tự động xuống dòng: ĐANG TẮT (Bấm để bật)');
        }
      });

      // 2. Copy Button
      const copyBtn = document.createElement('button');
      copyBtn.className = 'btn-code-action btn-copy';
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

      actions.appendChild(wrapBtn);
      actions.appendChild(copyBtn);
      headerEl.appendChild(actions);
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

        let widthVal = 800;
        let heightVal = 500;
        const viewBox = svgElement.getAttribute('viewBox');
        if (viewBox) {
          const parts = viewBox.split(/[\s,]+/).filter(Boolean).map(Number);
          if (parts.length === 4 && parts[2] > 0 && parts[3] > 0) {
            widthVal = parts[2];
            heightVal = parts[3];
          }
        } else {
          const bcr = svgElement.getBoundingClientRect();
          if (bcr.width > 0) widthVal = bcr.width;
          if (bcr.height > 0) heightVal = bcr.height;
        }

        // Clone and rename all IDs in defs/markers to prevent DOM collision and fix missing arrows
        let svgString = svgElement.outerHTML;
        const modalPrefix = 'lb-' + Math.floor(Math.random() * 100000) + '-';
        svgString = svgString.replace(/\bid="([^"]+)"/g, (match, id) => `id="${modalPrefix}${id}"`);
        svgString = svgString.replace(/url\(["']?#([^"')]+)["']?\)/g, (match, id) => `url(#${modalPrefix}${id})`);
        svgString = svgString.replace(/xlink:href=["']?#([^"')]+)["']?/g, (match, id) => `xlink:href="#${modalPrefix}${id}"`);
        svgString = svgString.replace(/href=["']?#([^"')]+)["']?/g, (match, id) => `href="#${modalPrefix}${id}"`);

        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = svgString;
        const clonedSvg = tempDiv.querySelector('svg');

        if (clonedSvg) {
          clonedSvg.setAttribute('width', widthVal);
          clonedSvg.setAttribute('height', heightVal);
          clonedSvg.style.width = `${widthVal}px`;
          clonedSvg.style.height = `${heightVal}px`;
          clonedSvg.style.maxWidth = 'none';
          clonedSvg.style.maxHeight = 'none';
          clonedSvg.style.display = 'block';
          clonedSvg.style.background = 'transparent';

          // Zero Solid Fill: Sanitize any dark or opaque fills on nodes, clusters, and actors
          clonedSvg.querySelectorAll('rect, polygon, circle, ellipse, path').forEach(el => {
            const fill = el.getAttribute('fill');
            if (fill && (
              fill.toLowerCase() === '#000000' || 
              fill.toLowerCase() === '#000' || 
              fill.toLowerCase() === '#1f2020' || 
              fill.toLowerCase() === '#0d1117' || 
              fill.toLowerCase() === '#1e293b' || 
              fill.toLowerCase() === '#333333' || 
              fill.toLowerCase() === '#222' || 
              fill.toLowerCase() === '#111' ||
              fill.toLowerCase() === '#ececff' ||
              fill.toLowerCase() === 'black'
            )) {
              el.setAttribute('fill', 'none');
            }
          });

          content.appendChild(clonedSvg);
        }

        scale = 1.1;
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
            scale = Math.max(0.3, scale - 0.25);
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
        scale = Math.max(0.3, scale - 0.25);
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
        const delta = e.deltaY > 0 ? -0.12 : 0.12;
        scale = Math.min(5, Math.max(0.3, scale + delta));
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
  }

  async function initMermaidDiagrams() {
    if (typeof mermaid === 'undefined') return;

    attachMermaidLightbox();

    const mermaidCodes = document.querySelectorAll(
      'code.language-mermaid, pre.language-mermaid, div.language-mermaid pre code, .highlighter-rouge.language-mermaid pre code, .language-mermaid pre'
    );

    if (mermaidCodes.length === 0) {
      return;
    }

    const isDark = document.documentElement.classList.contains('dark-theme');
    mermaid.initialize({
      startOnLoad: false,
      theme: isDark ? 'dark' : 'default',
      themeVariables: {
        darkMode: isDark,
        fontFamily: 'Plus Jakarta Sans, Inter, system-ui, -apple-system, sans-serif',
        fontSize: '13px',
        primaryTextColor: isDark ? '#f1f5f9' : '#0f172a',
        secondaryTextColor: isDark ? '#cbd5e1' : '#334155',
        lineColor: isDark ? '#94a3b8' : '#64748b',
        arrowheadColor: isDark ? '#94a3b8' : '#64748b',
        edgeLabelBackground: isDark ? '#1e293b' : '#f8fafc',
        clusterBkg: 'transparent',
        clusterBorder: isDark ? '#334155' : '#cbd5e1',
        mainBkg: 'transparent',
        nodeBkg: 'transparent',
        // Sequence Diagram Theme Variables
        actorBkg: 'transparent',
        actorBorder: isDark ? '#38bdf8' : '#0284c7',
        actorTextColor: isDark ? '#f8fafc' : '#0f172a',
        actorLineColor: isDark ? '#64748b' : '#94a3b8',
        signalColor: isDark ? '#94a3b8' : '#475569',
        signalTextColor: isDark ? '#f8fafc' : '#0f172a',
        labelBoxBkgColor: 'transparent',
        labelBoxBorderColor: isDark ? '#334155' : '#cbd5e1',
        labelTextColor: isDark ? '#f8fafc' : '#0f172a',
        loopTextColor: isDark ? '#f8fafc' : '#0f172a',
        noteBkgColor: isDark ? 'rgba(30, 41, 59, 0.85)' : 'rgba(241, 245, 249, 0.95)',
        noteBorderColor: isDark ? '#f59e0b' : '#d97706',
        noteTextColor: isDark ? '#fbbf24' : '#b45309',
        activationBorderColor: '#38bdf8',
        activationBkgColor: isDark ? 'rgba(56, 189, 248, 0.15)' : 'rgba(2, 132, 199, 0.1)',
        sequenceNumberColor: '#ffffff'
      },
      flowchart: {
        htmlLabels: true,
        curve: 'basis',
        padding: 24,
        nodeSpacing: 55,
        rankSpacing: 55,
        useMaxWidth: false
      },
      sequence: {
        actorMargin: 50,
        boxMargin: 10,
        boxTextMargin: 5,
        noteMargin: 10,
        messageMargin: 35,
        mirrorActors: false,
        bottomMarginAdj: 1,
        useMaxWidth: false,
        rightAngles: false,
        showSequenceNumbers: true
      },
      securityLevel: 'loose'
    });

    for (let i = 0; i < mermaidCodes.length; i++) {
      const codeEl = mermaidCodes[i];
      const rawContent = codeEl.textContent || codeEl.innerText;
      const container = codeEl.closest('.highlighter-rouge') || codeEl.closest('pre') || codeEl;

      const mermaidWrapper = document.createElement('div');
      mermaidWrapper.className = 'mermaid-wrapper';

      const mermaidInner = document.createElement('div');
      mermaidInner.className = 'mermaid';
      const renderId = 'mermaid-svg-' + i + '-' + Math.floor(Math.random() * 10000);

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

      try {
        const { svg } = await mermaid.render(renderId, rawContent.trim());
        mermaidInner.innerHTML = svg;
      } catch (err) {
        console.warn('Mermaid render error on diagram ' + i + ':', err);
        mermaidInner.textContent = rawContent.trim();
      }

      const clickHandler = (e) => {
        e.preventDefault();
        e.stopPropagation();
        const svg = mermaidInner.querySelector('svg');
        if (svg && window._openMermaidLightbox) {
          window._openMermaidLightbox(svg);
        }
      };

      zoomHint.addEventListener('click', clickHandler);
      mermaidInner.style.cursor = 'zoom-in';
      mermaidInner.addEventListener('click', clickHandler);
    }
  }

  /* ==========================================================================
     Article Enhancements: Convert GitHub Alerts & Responsive Tables
     ========================================================================== */
  function initArticleEnhancements() {
    const articleBody = document.querySelector('.article-body');
    if (!articleBody) return;

    // 1. Wrap all tables in .table-responsive if not already wrapped
    articleBody.querySelectorAll('table').forEach((table) => {
      if (!table.parentElement.classList.contains('table-responsive')) {
        const wrapper = document.createElement('div');
        wrapper.className = 'table-responsive';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
      }
    });

    // 2. Transform GitHub Alert Blockquotes (> [!WARNING], > [!IMPORTANT], etc.)
    const alertTypes = {
      'WARNING': {
        typeClass: 'callout-warning',
        title: 'CẢNH BÁO QUAN TRỌNG (WARNING)',
        icon: '<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>'
      },
      'IMPORTANT': {
        typeClass: 'callout-important',
        title: 'LƯU Ý CỐT LÕI (IMPORTANT)',
        icon: '<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
      },
      'TIP': {
        typeClass: 'callout-tip',
        title: 'MẸO THỰC CHIẾN (PRO TIP)',
        icon: '<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 18h6"></path><path d="M10 22h4"></path><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5.76.76 1.23 1.52 1.41 2.5"></path></svg>'
      },
      'NOTE': {
        typeClass: 'callout-note',
        title: 'GHI CHÚ (NOTE)',
        icon: '<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>'
      },
      'CAUTION': {
        typeClass: 'callout-caution',
        title: 'CHÚ Ý RỦI RO (CAUTION)',
        icon: '<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"></polygon><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>'
      }
    };

    articleBody.querySelectorAll('blockquote').forEach((bq) => {
      const text = bq.textContent.trim();
      const match = text.match(/^\[!(WARNING|IMPORTANT|TIP|NOTE|CAUTION|DANGER)\]/i);
      if (match) {
        let key = match[1].toUpperCase();
        if (key === 'DANGER') key = 'CAUTION';
        const meta = alertTypes[key] || alertTypes['NOTE'];

        let rawHtml = bq.innerHTML;
        rawHtml = rawHtml.replace(/\[!(WARNING|IMPORTANT|TIP|NOTE|CAUTION|DANGER)\]/i, '').trim();
        rawHtml = rawHtml.replace(/^(<br\s*\/?>|\s)+/i, '');

        const callout = document.createElement('div');
        callout.className = `callout-box ${meta.typeClass}`;
        callout.innerHTML = `
          <div class="callout-header">
            ${meta.icon}
            <span>${meta.title}</span>
          </div>
          <div class="callout-body">
            ${rawHtml}
          </div>
        `;
        bq.parentNode.replaceChild(callout, bq);
      }
    });

    // 3. Progressive render for raw markdown within Q&A cards if unparsed
    articleBody.querySelectorAll('.qa-answer, .qa-summary-left span').forEach((el) => {
      if (el.innerHTML.includes('**') || el.innerHTML.includes('`')) {
        let html = el.innerHTML;
        html = html.replace(/\*\*([^*]+)\*\*/g, '<b style="color: var(--accent-primary);">$1</b>');
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
        el.innerHTML = html;
      }
    });
  }

  // Initial enhancements & render
  initArticleEnhancements();
  initMermaidDiagrams();

  // Re-initialize MathJax if needed on dynamic changes
  if (window.MathJax && window.MathJax.typesetPromise) {
    window.MathJax.typesetPromise().catch((err) => console.warn('MathJax typesetting error:', err));
  }
});
