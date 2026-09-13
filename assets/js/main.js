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
          const rawText = code.innerText;
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
    const POSTS_PER_PAGE = 4;
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

      // Page Number Buttons
      for (let p = 1; p <= totalPages; p++) {
        const pageBtn = document.createElement('button');
        pageBtn.className = `page-btn ${p === currentPage ? 'active' : ''}`;
        pageBtn.textContent = p;
        pageBtn.type = 'button';
        pageBtn.setAttribute('aria-label', `Page ${p}`);
        pageBtn.addEventListener('click', () => {
          if (currentPage !== p) {
            currentPage = p;
            renderPagination();
            scrollToGrid();
          }
        });
        paginationControls.appendChild(pageBtn);
      }

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
});
