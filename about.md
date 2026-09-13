---
layout: page
title: "About"
permalink: /about.html
---

{% assign about = site.about_page %}

<!-- Author Spotlight Hero Card -->
<div class="about-hero-card" style="display: flex; gap: 2rem; align-items: center; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 2.25rem; box-shadow: var(--shadow-sm); margin-bottom: 3rem; flex-wrap: wrap;">
  {% if site.author.avatar %}
    <img src="{{ site.author.avatar | relative_url }}" alt="{{ site.author.name }}" style="width: 88px; height: 88px; border-radius: var(--radius-lg); object-fit: cover; box-shadow: var(--shadow-sm); border: 2px solid var(--border-color); display: block;">
  {% else %}
    <div class="author-avatar" style="width: 88px; height: 88px; font-size: 2rem; border-radius: var(--radius-lg);">
      {{ site.author.initials | default: "KN" }}
    </div>
  {% endif %}
  <div style="flex: 1; min-width: 280px;">
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem; flex-wrap: wrap;">
      <h2 style="font-size: 1.85rem; margin: 0; color: var(--text-primary);">{{ site.author.name }}</h2>
      <span class="badge badge--primary">{{ about.hero_badge | default: site.author.title }}</span>
    </div>
    <div style="font-size: 0.95rem; color: var(--accent-primary); font-weight: 600; margin-bottom: 0.65rem;">
      {{ site.author.subtitle }}
    </div>
    <div style="font-size: 0.875rem; color: var(--text-muted); display: flex; flex-wrap: wrap; gap: 1.25rem;">
      <span>📍 {{ site.author.location }}</span>
      <span>✉️ <a href="mailto:{{ site.author.email }}" style="color: inherit;">{{ site.author.email }}</a></span>
      {% if site.social.github %}
        <span>🐙 <a href="https://github.com/{{ site.social.github }}" target="_blank" rel="noopener noreferrer" style="color: inherit;">github.com/{{ site.social.github }}</a></span>
      {% endif %}
      {% if site.social.linkedin %}
        <span>💼 <a href="https://linkedin.com/in/{{ site.social.linkedin }}" target="_blank" rel="noopener noreferrer" style="color: inherit;">linkedin.com/in/{{ site.social.linkedin }}</a></span>
      {% endif %}
    </div>
  </div>
</div>

<!-- Section 1: Background & Philosophy -->
<h2>{{ about.background.section_title }}</h2>

{{ about.background.intro | markdownify }}

<h3>{{ about.background.focus_heading }}</h3>
<ul>
  {% for item in about.background.focus_items %}
    <li><strong>{{ item.title }}</strong> {{ item.desc }}</li>
  {% endfor %}
</ul>

<h3>{{ about.background.principles_heading }}</h3>
<ul>
  {% for p in about.background.principles %}
    <li><strong>{{ p.title }}</strong> {{ p.desc }}</li>
  {% endfor %}
</ul>

<hr style="margin: 3rem 0; border: 0; border-top: 1px solid var(--border-color);">

<!-- Section 2: Technical Competencies Matrix -->
<h2>{{ about.competencies.section_title }}</h2>

<div class="grid grid--2col" style="gap: 1.25rem; margin: 2rem 0;">
  {% for comp in about.competencies.items %}
    <div class="card" style="padding: 1.5rem;">
      <h4 style="margin: 0 0 0.75rem 0; font-size: 1.05rem; color: var(--text-primary);">{{ comp.title }}</h4>
      <p style="font-size: 0.925rem; margin-bottom: 0; color: var(--text-secondary);">
        {{ comp.skills }}
      </p>
    </div>
  {% endfor %}
</div>

<hr style="margin: 3rem 0; border: 0; border-top: 1px solid var(--border-color);">

<!-- Section 3: Professional Work Experience -->
<h2>{{ about.experience.section_title }}</h2>

<div class="timeline-wrapper" style="display: flex; flex-direction: column; gap: 2rem; margin: 2rem 0;">
  {% for job in about.experience.jobs %}
    <div class="card" style="padding: 1.75rem 2rem;">
      <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; margin-bottom: 0.25rem; gap: 0.5rem;">
        <h3 style="margin: 0; font-size: 1.25rem; color: var(--text-primary);">{{ job.role }}</h3>
        <span class="badge {{ job.badge_class | default: 'badge--primary' }}">{{ job.period }}</span>
      </div>
      <div style="font-size: 0.95rem; font-weight: 600; color: var(--accent-primary); margin-bottom: 1rem;">{{ job.company }}</div>
      <ul style="margin-left: 1.25rem; font-size: 0.95rem; display: flex; flex-direction: column; gap: 0.5rem; color: var(--text-secondary);">
        {% for bullet in job.highlights %}
          <li>{{ bullet }}</li>
        {% endfor %}
      </ul>
    </div>
  {% endfor %}
</div>

<hr style="margin: 3rem 0; border: 0; border-top: 1px solid var(--border-color);">

<!-- Section 4: Education, Certifications & Research -->
<h2>{{ about.education_and_certifications.section_title }}</h2>

<div class="grid grid--2col" style="gap: 1.5rem; margin: 2rem 0;">
  
  <!-- Education Card -->
  <div class="card" style="padding: 1.75rem;">
    <h3 style="margin-top: 0; font-size: 1.2rem; color: var(--text-primary); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
      {{ about.education_and_certifications.education.title }}
    </h3>
    <div style="margin-top: 1rem;">
      <strong>{{ about.education_and_certifications.education.degree }}</strong>
      <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.25rem;">
        {{ about.education_and_certifications.education.institution }}
      </div>
      <p style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0;">
        {{ about.education_and_certifications.education.desc }}
      </p>
    </div>
  </div>

  <!-- Certifications Card -->
  <div class="card" style="padding: 1.75rem;">
    <h3 style="margin-top: 0; font-size: 1.2rem; color: var(--text-primary); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
      {{ about.education_and_certifications.certifications.title }}
    </h3>
    <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.9rem;">
      {% for cert in about.education_and_certifications.certifications.items %}
        <div>{{ cert }}</div>
      {% endfor %}
    </div>
  </div>

</div>

<!-- Research Publications -->
{% if about.education_and_certifications.research %}
  <h3>{{ about.education_and_certifications.research.title }}</h3>
  <ul>
    {% for pub in about.education_and_certifications.research.items %}
      <li>📄 <strong>{{ pub.title }}</strong> {{ pub.name }}</li>
    {% endfor %}
  </ul>
{% endif %}

<hr style="margin: 3rem 0; border: 0; border-top: 1px solid var(--border-color);">

<!-- Download Resume & Call to Action Box -->
{% assign resume = about.resume_download %}
<div id="resume-download" class="card" style="margin-top: 3.5rem; padding: 2.5rem; text-align: center; background: linear-gradient(135deg, var(--bg-surface), var(--bg-subtle)); border: 1px solid rgba(var(--accent-primary-rgb), 0.35); box-shadow: var(--shadow-lg);">
  <div style="font-size: 2.25rem; margin-bottom: 0.5rem;">📄</div>
  <h2 style="font-size: 1.85rem; margin-top: 0; margin-bottom: 0.5rem;">{{ resume.title }}</h2>
  <p style="color: var(--text-secondary); max-width: 580px; margin: 0 auto 1.75rem auto; font-size: 1.05rem;">
    {{ resume.description }}
  </p>

  <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1.5rem;">
    <a href="{{ resume.pdf_url | relative_url }}" class="btn btn--accent" download style="padding: 0.75rem 1.75rem; font-size: 1rem;">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
      </svg>
      {{ resume.download_btn_text }}
    </a>

    <button onclick="window.print()" class="btn btn--secondary" style="padding: 0.75rem 1.5rem; font-size: 1rem;">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
      </svg>
      {{ resume.print_btn_text }}
    </button>
  </div>

  <div style="font-size: 0.9rem; color: var(--text-muted);">
    {{ resume.cta_text }} <a href="{{ resume.cta_link_url | relative_url }}" style="font-weight: 600;">{{ resume.cta_link_text }}</a>
  </div>
</div>
