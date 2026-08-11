document.addEventListener('DOMContentLoaded', () => {
  // Mobile Hamburger Toggle
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

    // Close menu when clicking links
    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('open');
        navMenu.classList.remove('open');
      });
    });
  }

  // Dark Mode Toggle Logic
  const themeToggle = document.getElementById('theme-toggle');
  
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const isDark = document.documentElement.classList.toggle('dark-theme');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
      
      // Accessibility update
      themeToggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    });
  }

  // Navbar blur/translucency on Scroll
  const header = document.querySelector('header.navbar');
  if (header) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 10) {
        header.style.boxShadow = 'var(--card-shadow)';
      } else {
        header.style.boxShadow = 'none';
      }
    });
  }

  // Inject Copy Button inside Kramdown (Rouge) Code blocks
  const codeBlocks = document.querySelectorAll('div.highlighter-rouge, figure.highlight');
  
  codeBlocks.forEach(wrapper => {
    // Determine language from class
    let lang = 'code';
    wrapper.classList.forEach(cls => {
      if (cls.startsWith('language-')) {
        lang = cls.replace('language-', '').toUpperCase();
      }
    });

    // Create header element if it doesn't already exist
    let headerEl = wrapper.querySelector('.code-header');
    if (!headerEl) {
      headerEl = document.createElement('div');
      headerEl.className = 'code-header';
      
      const langSpan = document.createElement('span');
      langSpan.textContent = lang;
      headerEl.appendChild(langSpan);

      const copyBtn = document.createElement('button');
      copyBtn.className = 'btn-copy';
      copyBtn.type = 'button';
      copyBtn.textContent = 'Copy';
      
      copyBtn.addEventListener('click', () => {
        const code = wrapper.querySelector('pre code') || wrapper.querySelector('pre');
        if (code) {
          const rawText = code.innerText;
          navigator.clipboard.writeText(rawText).then(() => {
            copyBtn.textContent = 'Copied!';
            copyBtn.style.color = 'var(--accent)';
            setTimeout(() => {
              copyBtn.textContent = 'Copy';
              copyBtn.style.color = '';
            }, 2000);
          }).catch(err => {
            console.error('Failed to copy text: ', err);
            copyBtn.textContent = 'Failed';
          });
        }
      });

      headerEl.appendChild(copyBtn);
      wrapper.insertBefore(headerEl, wrapper.firstChild);
    }
  });
});
