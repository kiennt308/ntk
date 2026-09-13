document.addEventListener('DOMContentLoaded', () => {
  /* ==========================================================================
     1. Toast Notification Utility
     ========================================================================== */
  function showToast(message) {
    let toast = document.getElementById('toast-notification');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'toast-notification';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 2500);
  }

  /* ==========================================================================
     2. Dark Mode Toggle Logic
     ========================================================================== */
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const isDark = document.documentElement.classList.toggle('dark-theme');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
      themeToggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    });
  }

  /* ==========================================================================
     3. Mobile Hamburger Menu
     ========================================================================== */
  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.querySelector('.nav-menu');

  if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      navMenu.classList.toggle('open');
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
        hamburger.classList.remove('open');
        navMenu.classList.remove('open');
      }
    });

    // Close menu when clicking navigation links
    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('open');
        navMenu.classList.remove('open');
      });
    });
  }

  /* ==========================================================================
     4. Reading Progress Bar & Header Shadow
     ========================================================================== */
  const progressBar = document.getElementById('reading-progress');
  const header = document.querySelector('header.navbar');
  const articleMain = document.querySelector('.article-main');

  window.addEventListener('scroll', () => {
    // Header shadow on scroll
    if (header) {
      if (window.scrollY > 15) {
        header.style.boxShadow = 'var(--shadow-md)';
      } else {
        header.style.boxShadow = 'none';
      }
    }

    // Article reading progress calculation
    if (progressBar && articleMain) {
      const articleRect = articleMain.getBoundingClientRect();
      const articleTop = articleMain.offsetTop;
      const articleHeight = articleMain.offsetHeight;
      const windowHeight = window.innerHeight;
      const scrollPos = window.scrollY;

      const progress = Math.min(
        100,
        Math.max(0, ((scrollPos - articleTop + windowHeight * 0.4) / (articleHeight - windowHeight * 0.4)) * 100)
      );
      progressBar.style.width = `${progress}%`;
    }
  });

  /* ==========================================================================
     5. Kramdown Code Block Headers & Copy Functionality
     ========================================================================== */
  const codeBlocks = document.querySelectorAll('div.highlighter-rouge, figure.highlight');
  
  codeBlocks.forEach(wrapper => {
    let lang = 'CODE';
    wrapper.classList.forEach(cls => {
      if (cls.startsWith('language-')) {
        lang = cls.replace('language-', '').toUpperCase();
      }
    });

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
      langSpan.textContent = lang;

      leftCol.appendChild(dots);
      leftCol.appendChild(langSpan);
      headerEl.appendChild(leftCol);

      const copyBtn = document.createElement('button');
      copyBtn.className = 'btn-copy';
      copyBtn.type = 'button';
      copyBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
        <span>Copy</span>
      `;
      
      copyBtn.addEventListener('click', () => {
        const code = wrapper.querySelector('pre code') || wrapper.querySelector('pre');
        if (code) {
          const rawText = code.innerText;
          navigator.clipboard.writeText(rawText).then(() => {
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
     6. Copy Page URL / Share Button
     ========================================================================== */
  const copyLinkButtons = document.querySelectorAll('.btn-copy-link');
  copyLinkButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const url = window.location.href;
      navigator.clipboard.writeText(url).then(() => {
        showToast('Article link copied to clipboard!');
      }).catch(() => {
        showToast('Failed to copy link.');
      });
    });
  });

  /* ==========================================================================
     7. Live Blog Category Filtering, Instant Search & Dynamic Pagination (blog.html)
     ========================================================================== */
  const filterButtons = document.querySelectorAll('.live-filter-btn');
  const postCards = Array.from(document.querySelectorAll('.post-card-item'));
  const blogSearchInput = document.getElementById('blog-live-search');
  const postCountDisplay = document.getElementById('visible-post-count');
  const paginationWrapper = document.getElementById('blog-pagination');
  const paginationControls = document.getElementById('pagination-controls');
  const postsGrid = document.getElementById('posts-grid');

  if (postCards.length > 0) {
    const POSTS_PER_PAGE = 4; // 4 bài viết trên mỗi trang cho bố cục 2 cột thoáng đẹp
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
        emptyNotice.style.display = totalPosts === 0 ? 'block' : 'none';
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
        const categories = (card.getAttribute('data-categories') || '').toLowerCase();
        const tags = (card.getAttribute('data-tags') || '').toLowerCase();
        const title = (card.getAttribute('data-title') || '').toLowerCase();
        const desc = (card.getAttribute('data-desc') || '').toLowerCase();

        const matchesCategory = currentCategory === 'all' || categories.includes(currentCategory);
        const matchesSearch = !searchQuery || 
          title.includes(searchQuery) || 
          desc.includes(searchQuery) || 
          tags.includes(searchQuery) || 
          categories.includes(searchQuery);

        return matchesCategory && matchesSearch;
      });

      currentPage = 1; // Reset to page 1 on category/search query changes
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
      blogSearchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.trim().toLowerCase();
        updateFilteredPosts();
      });
    }

    // Sidebar filter triggers
    const sidebarTriggers = document.querySelectorAll('.sidebar-filter-trigger');
    sidebarTriggers.forEach(trigger => {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        const filterVal = trigger.getAttribute('data-filter')?.toLowerCase();
        const targetBtn = Array.from(filterButtons).find(b => b.getAttribute('data-filter')?.toLowerCase() === filterVal);
        if (targetBtn) {
          targetBtn.click();
          scrollToGrid();
        }
      });
    });

    // Check URL hash for initial filter on load (e.g. blog.html#aws)
    if (window.location.hash) {
      const hash = window.location.hash.replace('#', '').toLowerCase();
      const targetBtn = Array.from(filterButtons).find(b => b.getAttribute('data-filter')?.toLowerCase() === hash);
      if (targetBtn) {
        targetBtn.click();
      } else {
        updateFilteredPosts();
      }
    } else {
      updateFilteredPosts();
    }
  }
});
