---
layout: page
title: "Get in Touch"
permalink: /contact.html
---

<p style="font-size: 1.1rem; color: var(--text-secondary); margin-bottom: 3rem; text-align: center; max-width: 600px; margin-left: auto; margin-right: auto;">
  Have a technical question, a project collaboration idea, or looking to discuss cloud scalability? Reach out through any of the channels below.
</p>

<div class="contact-grid">
  <!-- Interactive Form Placeholders -->
  <div class="card" style="padding: 2rem;">
    <h3 style="margin-top: 0; margin-bottom: 1.5rem; font-size: 1.25rem;">Send a Message</h3>
    
    <form onsubmit="event.preventDefault(); alert('This is a static site! Please email me directly at kien.nguyen@example.com.');" style="display: flex; flex-direction: column; gap: 1.25rem;">
      <div>
        <label for="name" style="display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-primary);">Name</label>
        <input type="text" id="name" placeholder="John Doe" class="search-input" style="padding: 0.65rem 1rem;" required>
      </div>
      
      <div>
        <label for="email" style="display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-primary);">Email Address</label>
        <input type="email" id="email" placeholder="john@example.com" class="search-input" style="padding: 0.65rem 1rem;" required>
      </div>

      <div>
        <label for="message" style="display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-primary);">Message</label>
        <textarea id="message" rows="5" placeholder="Your message here..." class="search-input" style="padding: 0.65rem 1rem; resize: vertical; font-family: var(--font-sans);" required></textarea>
      </div>

      <button type="submit" class="btn btn--accent" style="width: 100%; padding: 0.65rem;">Send Message</button>
    </form>
  </div>

  <!-- Social Link Deck -->
  <div style="display: flex; flex-direction: column; gap: 1.5rem;">
    
    <div class="card" style="padding: 1.5rem; flex-direction: row; align-items: center; gap: 1.5rem;">
      <div class="cert-icon" style="color: var(--accent); border-color: rgba(var(--accent-rgb), 0.2); background: rgba(var(--accent-rgb), 0.05);">
        @
      </div>
      <div>
        <h4 style="margin: 0; font-size: 1.05rem;">Email Address</h4>
        <a href="mailto:kien.nguyen@example.com" style="font-size: 0.9rem; font-weight: 500;">kien.nguyen@example.com</a>
      </div>
    </div>

    <div class="card" style="padding: 1.5rem; flex-direction: row; align-items: center; gap: 1.5rem;">
      <div class="cert-icon" style="color: var(--primary); border-color: rgba(var(--primary-rgb), 0.2); background: rgba(var(--primary-rgb), 0.05);">
        GH
      </div>
      <div>
        <h4 style="margin: 0; font-size: 1.05rem;">GitHub Profile</h4>
        <a href="https://github.com/kiennt308" target="_blank" rel="noopener noreferrer" style="font-size: 0.9rem; font-weight: 500;">github.com/kiennt308</a>
      </div>
    </div>

    <div class="card" style="padding: 1.5rem; flex-direction: row; align-items: center; gap: 1.5rem;">
      <div class="cert-icon" style="color: var(--primary); border-color: rgba(var(--primary-rgb), 0.2); background: rgba(var(--primary-rgb), 0.05);">
        IN
      </div>
      <div>
        <h4 style="margin: 0; font-size: 1.05rem;">LinkedIn Profile</h4>
        <a href="https://linkedin.com/in/kiennt308" target="_blank" rel="noopener noreferrer" style="font-size: 0.9rem; font-weight: 500;">linkedin.com/in/kiennt308</a>
      </div>
    </div>

  </div>
</div>
