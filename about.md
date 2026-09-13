---
layout: default
title: "About Kien Nguyen | Senior DevOps Engineer & Cloud Architect"
permalink: /about.html
---

{% assign about = site.about_page %}

<div class="container container--narrow" style="margin-top: 1rem;">

<!-- Author Spotlight Hero Card -->
<div class="about-hero-card" style="display: flex; gap: 2rem; align-items: center; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 2.25rem; box-shadow: var(--shadow-sm); margin-bottom: 2.5rem; flex-wrap: wrap;">
  {% if site.author.avatar %}
    <img src="{{ site.author.avatar | relative_url }}" alt="{{ site.author.name }}" style="width: 96px; height: 96px; border-radius: var(--radius-lg); object-fit: cover; box-shadow: var(--shadow-md); border: 2px solid var(--border-color); display: block; flex-shrink: 0;">
  {% else %}
    <div class="author-avatar" style="width: 96px; height: 96px; font-size: 2.25rem; border-radius: var(--radius-lg); flex-shrink: 0;">
      {{ site.author.initials | default: "KN" }}
    </div>
  {% endif %}
  <div style="flex: 1; min-width: 280px;">
    <div style="display: flex; align-items: center; gap: 0.65rem; margin-bottom: 0.35rem; flex-wrap: wrap;">
      <h1 style="font-size: 1.85rem; margin: 0; color: var(--text-primary); font-weight: 800;">{{ site.author.name }}</h1>
      <span class="badge badge--primary">{{ about.hero_badge | default: "Senior DevOps Engineer" }}</span>
      <span class="badge badge--emerald" style="font-size: 0.75rem;">10+ Yrs IT Exp</span>
      <span class="badge badge--amber" style="font-size: 0.75rem;">15 Certifications</span>
    </div>
    <div style="font-size: 0.98rem; color: var(--accent-primary); font-weight: 600; margin-bottom: 0.75rem;">
      {{ site.author.subtitle | default: "AWS Cloud | Terraform, Kubernetes, CI/CD | Scalable Cloud Platforms" }}
    </div>
    <div style="font-size: 0.875rem; color: var(--text-muted); display: flex; flex-wrap: wrap; gap: 1.25rem; align-items: center;">
      <span style="display: inline-flex; align-items: center; gap: 0.35rem;">
        {% include icon.html name="map-pin" size=14 %}
        <span>{{ site.author.location | default: "Ho Chi Minh City, Vietnam" }}</span>
      </span>
      <span style="display: inline-flex; align-items: center; gap: 0.35rem;">
        {% include icon.html name="mail" size=14 %}
        <a href="mailto:{{ site.author.email }}" style="color: inherit;">{{ site.author.email }}</a>
      </span>
      {% if site.social.github %}
        <span style="display: inline-flex; align-items: center; gap: 0.35rem;">
          {% include icon.html name="github" size=14 %}
          <a href="https://github.com/{{ site.social.github }}" target="_blank" rel="noopener noreferrer" style="color: inherit;">github.com/{{ site.social.github }}</a>
        </span>
      {% endif %}
      {% if site.social.linkedin %}
        <span style="display: inline-flex; align-items: center; gap: 0.35rem;">
          {% include icon.html name="briefcase" size=14 %}
          <a href="https://linkedin.com/in/{{ site.social.linkedin }}" target="_blank" rel="noopener noreferrer" style="color: inherit;">linkedin.com/in/{{ site.social.linkedin }}</a>
        </span>
      {% endif %}
    </div>
  </div>
</div>

<!-- Section 1: Professional Summary & Philosophy -->
<h2>{{ about.background.section_title }}</h2>

{{ about.background.intro | markdownify }}

<h3 style="margin-top: 2rem;">{{ about.background.focus_heading }}</h3>
<ul style="list-style: none; padding-left: 0; display: flex; flex-direction: column; gap: 1rem;">
  {% for item in about.background.focus_items %}
    <li style="display: flex; align-items: flex-start; gap: 0.85rem;">
      <div style="width: 36px; height: 36px; border-radius: var(--radius-md); background: var(--bg-subtle); border: 1px solid var(--border-color); display: inline-flex; align-items: center; justify-content: center; color: var(--accent-primary); flex-shrink: 0; margin-top: 0.15rem;">
        {% include icon.html name=item.icon size=18 %}
      </div>
      <div style="line-height: 1.6;">
        <strong style="color: var(--text-primary);">{{ item.title }}</strong> {{ item.desc }}
      </div>
    </li>
  {% endfor %}
</ul>

<h3 style="margin-top: 2rem;">{{ about.background.principles_heading }}</h3>
<ul>
  {% for p in about.background.principles %}
    <li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">{{ p.title }}</strong> {{ p.desc }}</li>
  {% endfor %}
</ul>

<hr style="margin: 3rem 0; border: 0; border-top: 1px solid var(--border-color);">

<!-- Section 2: Technical Competencies Matrix -->
<h2>{{ about.competencies.section_title }}</h2>

<div class="grid grid--2col" style="gap: 1.25rem; margin: 2rem 0;">
  {% for comp in about.competencies.items %}
    <div class="card" style="padding: 1.5rem;">
      <div style="display: flex; align-items: center; gap: 0.65rem; margin-bottom: 0.85rem;">
        <div style="width: 36px; height: 36px; border-radius: var(--radius-md); background: var(--bg-subtle); border: 1px solid var(--border-color); display: inline-flex; align-items: center; justify-content: center; color: var(--accent-primary); flex-shrink: 0;">
          {% include icon.html name=comp.icon size=18 %}
        </div>
        <h4 style="margin: 0; font-size: 1.05rem; color: var(--text-primary);">{{ comp.title }}</h4>
      </div>
      <p style="font-size: 0.925rem; margin-bottom: 0; color: var(--text-secondary); line-height: 1.6;">
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
        <h3 style="margin: 0; font-size: 1.25rem; color: var(--text-primary); font-weight: 750;">{{ job.role }}</h3>
        <span class="badge {{ job.badge_class | default: 'badge--primary' }}">{{ job.period }}</span>
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 1rem; gap: 0.5rem;">
        <div style="font-size: 0.98rem; font-weight: 700; color: var(--accent-primary);">{{ job.company }}</div>
        {% if job.location %}
          <div style="font-size: 0.85rem; color: var(--text-muted); display: inline-flex; align-items: center; gap: 0.35rem;">
            {% include icon.html name="map-pin" size=12 %}
            <span>{{ job.location }}</span>
          </div>
        {% endif %}
      </div>
      <ul style="margin-left: 1.25rem; font-size: 0.95rem; display: flex; flex-direction: column; gap: 0.6rem; color: var(--text-secondary); line-height: 1.6;">
        {% for bullet in job.highlights %}
          <li>{{ bullet }}</li>
        {% endfor %}
      </ul>
    </div>
  {% endfor %}
</div>

<!-- Featured Executive Endorsement Card -->
{% if about.recommendation %}
<div class="card" style="margin: 3rem 0; padding: 2rem 2.25rem; background: linear-gradient(135deg, var(--bg-surface), var(--bg-subtle)); border-left: 4px solid var(--accent-primary); box-shadow: var(--shadow-md);">
  <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
    <div style="width: 36px; height: 36px; border-radius: var(--radius-md); background: var(--bg-subtle); border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center; color: var(--accent-primary); flex-shrink: 0;">
      {% include icon.html name="zap" size=18 %}
    </div>
    <div>
      <h3 style="margin: 0; font-size: 1.15rem; color: var(--text-primary);">{{ about.recommendation.section_title }}</h3>
      <div style="font-size: 0.85rem; color: var(--text-muted);">{{ about.recommendation.relationship }}</div>
    </div>
  </div>
  <blockquote style="margin: 0 0 1.25rem 0; padding: 0; border: none; background: transparent; font-size: 0.95rem; line-height: 1.7; color: var(--text-secondary); font-style: italic;">
    "{{ about.recommendation.quote }}"
  </blockquote>
  <div style="text-align: right; font-size: 0.9rem;">
    <strong style="color: var(--text-primary);">{{ about.recommendation.author_name }}</strong>
    <span style="color: var(--text-muted);"> — {{ about.recommendation.author_title }}</span>
  </div>
</div>
{% endif %}

<hr style="margin: 3rem 0; border: 0; border-top: 1px solid var(--border-color);">

<!-- Section 4: Education & Certifications -->
<h2>{{ about.education_and_certifications.section_title }}</h2>

<!-- Education Cards Grid -->
<h3 style="margin-top: 1.5rem;">{{ about.education_and_certifications.education.title }}</h3>
<div class="grid grid--2col" style="gap: 1.5rem; margin: 1.5rem 0 2.5rem 0;">
  {% for edu in about.education_and_certifications.education.degrees %}
    <div class="card" style="padding: 1.75rem;">
      <div style="display: flex; align-items: center; gap: 0.85rem; margin-bottom: 0.75rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem;">
        <div style="width: 46px; height: 46px; border-radius: var(--radius-md); background: var(--bg-subtle); border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center; padding: 4px; flex-shrink: 0; box-shadow: var(--shadow-sm);">
          <img src="{{ '/assets/imgs/logobachkhoasang.png' | relative_url }}" alt="Bach Khoa University" style="width: 100%; height: 100%; object-fit: contain;">
        </div>
        <div style="flex: 1;">
          <h4 style="margin: 0; font-size: 1.05rem; color: var(--text-primary); line-height: 1.35;">{{ edu.degree }}</h4>
          <span class="badge badge--primary" style="font-size: 0.72rem; margin-top: 0.35rem;">{{ edu.period }}</span>
        </div>
      </div>
      <div>
        <div style="font-size: 0.925rem; font-weight: 600; color: var(--accent-primary); margin-bottom: 0.35rem;">
          {{ edu.institution }}
        </div>
        <p style="font-size: 0.885rem; color: var(--text-secondary); margin-bottom: 0; line-height: 1.5;">
          {{ edu.desc }}
        </p>
      </div>
    </div>
  {% endfor %}
</div>

<!-- Certifications Grid -->
<h3>{{ about.education_and_certifications.certifications.title }}</h3>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 1.25rem; margin: 1.5rem 0 2.5rem 0;">
  {% for cert in about.education_and_certifications.certifications.items %}
    <div class="card cert-card" style="padding: 1.25rem; display: flex; align-items: center; gap: 1.15rem; transition: transform 0.2s ease, box-shadow 0.2s ease;">
      <!-- Badge Image Container -->
      <div style="width: 72px; height: 72px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; background: var(--bg-subtle); border-radius: var(--radius-md); border: 1px solid var(--border-color); padding: 0.35rem; box-shadow: var(--shadow-sm);">
        {% if cert.badge_image %}
          <img src="{{ cert.badge_image | relative_url }}" alt="{{ cert.name }}" style="width: 100%; height: 100%; object-fit: contain; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.15));" loading="lazy">
        {% else %}
          {% include icon.html name="shield" size=32 %}
        {% endif %}
      </div>

      <!-- Cert Info -->
      <div style="flex: 1; min-width: 0;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.35rem; margin-bottom: 0.25rem;">
          <h4 style="font-size: 0.95rem; font-weight: 750; color: var(--text-primary); margin: 0; line-height: 1.35;">
            {{ cert.name }}
          </h4>
          <span class="badge {% if cert.badge == 'Active' %}badge--emerald{% elsif cert.badge == 'Verified' %}badge--cyan{% elsif cert.badge == 'Trainer' %}badge--amber{% else %}badge--secondary{% endif %}" style="font-size: 0.65rem; flex-shrink: 0;">
            {{ cert.badge }}
          </span>
        </div>
        <div style="font-size: 0.825rem; color: var(--accent-primary); font-weight: 600; margin-bottom: 0.35rem;">
          {{ cert.issuer }}
        </div>
        <div style="font-size: 0.76rem; color: var(--text-muted); display: flex; justify-content: space-between; align-items: center; border-top: 1px dashed var(--border-color); padding-top: 0.35rem; gap: 0.5rem; flex-wrap: wrap;">
          <span>{{ cert.period }}</span>
          {% if cert.id %}
            <span title="Credential ID: {{ cert.id }}" style="font-family: var(--font-mono); font-size: 0.72rem; opacity: 0.85;">ID: {{ cert.id | truncate: 14 }}</span>
          {% endif %}
        </div>
      </div>
    </div>
  {% endfor %}
</div>

<!-- Languages Section -->
{% if about.education_and_certifications.languages %}
  <h3>{{ about.education_and_certifications.languages.title }}</h3>
  <div class="grid grid--2col" style="gap: 1rem; margin: 1rem 0 2.5rem 0;">
    {% for lang in about.education_and_certifications.languages.items %}
      <div class="card" style="padding: 1.25rem; display: flex; align-items: center; gap: 1rem;">
        <div style="width: 36px; height: 36px; border-radius: var(--radius-md); background: var(--bg-subtle); border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center; color: var(--accent-primary); flex-shrink: 0;">
          {% include icon.html name="code" size=18 %}
        </div>
        <div>
          <div style="font-weight: 700; color: var(--text-primary); font-size: 1rem;">{{ lang.name }}</div>
          <div style="font-size: 0.85rem; color: var(--text-muted);">{{ lang.level }}</div>
        </div>
      </div>
    {% endfor %}
  </div>
{% endif %}

<hr style="margin: 3rem 0; border: 0; border-top: 1px solid var(--border-color);">

<!-- Download Resume & Call to Action Box -->
{% assign resume = about.resume_download %}
<div id="resume-download" class="card" style="margin-top: 3.5rem; padding: 2.5rem; text-align: center; background: linear-gradient(135deg, var(--bg-surface), var(--bg-subtle)); border: 1px solid rgba(var(--accent-primary-rgb), 0.35); box-shadow: var(--shadow-lg);">
  <div style="margin-bottom: 0.75rem; color: var(--accent-primary); display: flex; justify-content: center;">
    <div style="width: 56px; height: 56px; border-radius: var(--radius-lg); background: var(--bg-surface); border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center; box-shadow: var(--shadow-sm);">
      {% include icon.html name="book" size=28 %}
    </div>
  </div>
  <h2 style="font-size: 1.85rem; margin-top: 0; margin-bottom: 0.5rem; font-weight: 800;">{{ resume.title }}</h2>
  <p style="color: var(--text-secondary); max-width: 600px; margin: 0 auto 1.75rem auto; font-size: 1.02rem; line-height: 1.6;">
    {{ resume.description }}
  </p>

  <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1.5rem;">
    <a href="https://linkedin.com/in/kiennt308" target="_blank" rel="noopener noreferrer" class="btn btn--accent" style="padding: 0.75rem 1.75rem; font-size: 1rem;">
      {% include icon.html name="briefcase" size=18 %}
      Connect on LinkedIn
    </a>

    <button onclick="window.print()" class="btn btn--secondary" style="padding: 0.75rem 1.5rem; font-size: 1rem;">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
      </svg>
      {{ resume.print_btn_text | default: "Print Profile" }}
    </button>
  </div>

  <div style="font-size: 0.925rem; color: var(--text-muted);">
    {{ resume.cta_text }} <a href="{{ resume.cta_link_url | relative_url }}" style="font-weight: 700; color: var(--accent-primary);">{{ resume.cta_link_text }}</a>
  </div>
</div>

</div>
