---
layout: page
title: "Get in Touch"
permalink: /contact.html
---

<p style="font-size: 1.15rem; color: var(--text-secondary); margin-bottom: 3rem; text-align: center; max-width: 650px; margin-left: auto; margin-right: auto;">
  Have a technical question, looking to discuss cloud scalability, or interested in platform engineering consulting? Reach out directly through any of the channels below.
</p>

<div class="contact-grid">
  <!-- Interactive Form Placeholders -->
  <div class="card" style="padding: 2.25rem;">
    <h3 style="margin-top: 0; margin-bottom: 1.5rem; font-size: 1.35rem;">Send a Message</h3>
    
    <form onsubmit="event.preventDefault(); alert('Please email me directly at kiennt.sg@gmail.com!');" style="display: flex; flex-direction: column; gap: 1.25rem;">
      <div>
        <label for="name" style="display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-primary);">Name</label>
        <input type="text" id="name" placeholder="Your Name" class="search-input-box" style="padding: 0.75rem 1.25rem; border-radius: var(--radius-md);" required>
      </div>
      
      <div>
        <label for="email" style="display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-primary);">Email Address</label>
        <input type="email" id="email" placeholder="you@company.com" class="search-input-box" style="padding: 0.75rem 1.25rem; border-radius: var(--radius-md);" required>
      </div>

      <div>
        <label for="message" style="display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-primary);">Message</label>
        <textarea id="message" rows="5" placeholder="Let's talk about cloud architecture, Kubernetes, or SRE..." class="search-input-box" style="padding: 0.75rem 1.25rem; border-radius: var(--radius-md); resize: vertical; font-family: var(--font-sans);" required></textarea>
      </div>

      <button type="submit" class="btn btn--primary" style="width: 100%; padding: 0.85rem;">Send Message</button>
    </form>
  </div>

  <!-- Social Link Deck -->
  <div style="display: flex; flex-direction: column; gap: 1.5rem;">
    
    <div class="card" style="padding: 1.75rem; flex-direction: row; align-items: center; gap: 1.5rem;">
      <div style="width: 52px; height: 52px; border-radius: var(--radius-md); background: var(--accent-amber-light); color: var(--accent-amber); display: flex; align-items: center; justify-content: center; font-size: 1.35rem; font-weight: 700; flex-shrink: 0;">
        @
      </div>
      <div>
        <h4 style="margin: 0 0 0.25rem 0; font-size: 1.1rem;">Direct Email</h4>
        <a href="mailto:{{ site.email }}" style="font-size: 0.95rem; font-weight: 500;">{{ site.email }}</a>
      </div>
    </div>

    <div class="card" style="padding: 1.75rem; flex-direction: row; align-items: center; gap: 1.5rem;">
      <div style="width: 52px; height: 52px; border-radius: var(--radius-md); background: var(--accent-primary-light); color: var(--accent-primary); display: flex; align-items: center; justify-content: center; font-size: 1.35rem; font-weight: 700; flex-shrink: 0;">
        GH
      </div>
      <div>
        <h4 style="margin: 0 0 0.25rem 0; font-size: 1.1rem;">GitHub Profile</h4>
        <a href="https://github.com/{{ site.social.github }}" target="_blank" rel="noopener noreferrer" style="font-size: 0.95rem; font-weight: 500;">github.com/{{ site.social.github }}</a>
      </div>
    </div>

    <div class="card" style="padding: 1.75rem; flex-direction: row; align-items: center; gap: 1.5rem;">
      <div style="width: 52px; height: 52px; border-radius: var(--radius-md); background: var(--accent-cyan-light); color: var(--accent-cyan); display: flex; align-items: center; justify-content: center; font-size: 1.35rem; font-weight: 700; flex-shrink: 0;">
        IN
      </div>
      <div>
        <h4 style="margin: 0 0 0.25rem 0; font-size: 1.1rem;">LinkedIn Network</h4>
        <a href="https://linkedin.com/in/{{ site.social.linkedin }}" target="_blank" rel="noopener noreferrer" style="font-size: 0.95rem; font-weight: 500;">linkedin.com/in/{{ site.social.linkedin }}</a>
      </div>
    </div>

  </div>
</div>
