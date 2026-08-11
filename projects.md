---
layout: default
title: "Technical Projects"
permalink: /projects.html
---

<div class="container" style="margin-top: 2rem;">
  <div style="margin-bottom: 3.5rem; text-align: center;">
    <h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">Technical Projects</h1>
    <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto;">
      A showcase of production-grade platform systems, infrastructure-as-code libraries, and architectural frameworks.
    </p>
  </div>

  <div class="grid grid--2col">
    {% if site.data.projects.size > 0 %}
      {% for project in site.data.projects %}
        {% include project-card.html project=project %}
      {% endfor %}
    {% else %}
      <p style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 4rem 0;">No projects listed yet.</p>
    {% endif %}
  </div>
</div>
