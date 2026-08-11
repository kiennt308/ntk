---
layout: default
title: "Professional Timeline"
permalink: /experience.html
---

<div class="container" style="margin-top: 2rem;">
  <div style="margin-bottom: 3.5rem; text-align: center;">
    <h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">Work Experience</h1>
    <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto;">
      A chronicle of architecting cloud systems, deploying automation systems, and scaling operational processes.
    </p>
  </div>

  <div class="timeline">
    {% if site.data.experience.size > 0 %}
      {% for job in site.data.experience %}
        <div class="timeline-item">
          <div class="timeline-date">{{ job.date }}</div>
          <h2 class="timeline-title" style="margin-top: 0; margin-bottom: 0.25rem; font-size: 1.35rem;">{{ job.role }}</h2>
          <div class="timeline-subtitle">
            {{ job.company }}
          </div>
          <div class="timeline-body">
            <ul>
              {% for bullet in job.bullets %}
                <li>{{ bullet }}</li>
              {% endfor %}
            </ul>
          </div>
        </div>
      {% endfor %}
    {% else %}
      <p style="text-align: center; color: var(--text-muted); padding: 4rem 0;">No experience items listed yet.</p>
    {% endif %}
  </div>
</div>
