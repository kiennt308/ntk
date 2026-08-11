---
layout: default
title: "Technical Skills"
permalink: /skills.html
---

<div class="container" style="margin-top: 2rem;">
  <div style="margin-bottom: 3.5rem; text-align: center;">
    <h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">Technical Skills</h1>
    <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto;">
      A breakdown of tools, platforms, programming languages, and operations methodologies in my core competency.
    </p>
  </div>

  <div class="grid grid--2col">
    {% if site.data.skills.size > 0 %}
      {% for category in site.data.skills %}
        <div class="card">
          <h3 class="card__title" style="margin-top: 0; font-size: 1.25rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 1.25rem; color: var(--primary);">
            {{ category.name }}
          </h3>
          <div class="card__tags">
            {% for skill in category.skills %}
              <span class="badge badge--accent" style="font-weight: 500;">{{ skill }}</span>
            {% endfor %}
          </div>
        </div>
      {% endfor %}
    {% else %}
      <p style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 4rem 0;">No skills listed yet.</p>
    {% endif %}
  </div>
</div>
