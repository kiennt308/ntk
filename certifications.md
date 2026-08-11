---
layout: default
title: "Technical Certifications"
permalink: /certifications.html
---

<div class="container" style="margin-top: 2rem;">
  <div style="margin-bottom: 3.5rem; text-align: center;">
    <h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">Certifications</h1>
    <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto;">
      Validated expertise in cloud operations, security, container orchestration, and solutions architecture.
    </p>
  </div>

  <div class="cert-grid">
    {% if site.data.certifications.size > 0 %}
      {% for cert in site.data.certifications %}
        <div class="cert-card">
          <div class="cert-icon">
            {{ cert.badge_text }}
          </div>
          <div class="cert-info">
            <h3>{{ cert.name }}</h3>
            <p>
              {{ cert.issuer }} &middot; Issued {{ cert.date }}
            </p>
            {% if cert.id %}
              <p style="font-family: var(--font-mono); font-size: 0.8rem; margin-top: 0.15rem; color: var(--text-muted);">
                Credential ID: {{ cert.id }}
              </p>
            {% endif %}
            {% if cert.url %}
              <a href="{{ cert.url }}" target="_blank" rel="noopener noreferrer" style="font-size: 0.8rem; font-weight: 600; display: inline-block; margin-top: 0.5rem;">
                Verify Credential &rarr;
              </a>
            {% endif %}
          </div>
        </div>
      {% endfor %}
    {% else %}
      <p style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 4rem 0;">No certifications listed yet.</p>
    {% endif %}
  </div>
</div>
