---
layout: page
title: "Contact"
permalink: /contact.html
---

{% assign contact = site.contact_page %}

<div style="text-align: center; max-width: 650px; margin: 0 auto 3.5rem auto;">
  <span class="badge badge--primary" style="margin-bottom: 0.75rem;">{{ contact.badge | default: "CONTACT & CONNECT" }}</span>
  <h2 style="font-size: 2.25rem; font-weight: 800; margin-top: 0; margin-bottom: 0.75rem;">{{ contact.title }}</h2>
  <p style="font-size: 1.15rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 0;">
    {{ contact.subtitle }}
  </p>
</div>

<div class="grid grid--2col" style="gap: 1.5rem; margin-bottom: 3.5rem;">
  
  {% for channel in contact.channels %}
    <div class="card" style="padding: 2rem; display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem;">
          <div style="width: 52px; height: 52px; border-radius: var(--radius-md); background: {{ channel.icon_bg }}; color: {{ channel.icon_color }}; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 700;">
            {{ channel.icon }}
          </div>
          <span class="badge {{ channel.badge_class }}">{{ channel.badge }}</span>
        </div>
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.25rem; color: var(--text-primary);">{{ channel.title }}</h3>
        <p style="font-size: 0.95rem; color: var(--text-secondary); margin-bottom: 1.25rem;">
          {{ channel.desc }}
        </p>
      </div>

      <div style="padding-top: 1rem; border-top: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
        {% if channel.type == "email" %}
          <a href="mailto:{{ site.author.email }}" style="font-weight: 600; font-size: 1rem;">{{ site.author.email }}</a>
          <a href="mailto:{{ site.author.email }}" class="btn btn--primary btn--sm">{{ channel.btn_text }}</a>
        {% elsif channel.type == "linkedin" %}
          <span style="font-weight: 600; font-size: 1rem; color: var(--text-secondary);">linkedin.com/in/{{ site.social.linkedin }}</span>
          <a href="https://linkedin.com/in/{{ site.social.linkedin }}" target="_blank" rel="noopener noreferrer" class="btn btn--secondary btn--sm">{{ channel.btn_text }}</a>
        {% elsif channel.type == "github" %}
          <span style="font-weight: 600; font-size: 1rem; color: var(--text-secondary);">github.com/{{ site.social.github }}</span>
          <a href="https://github.com/{{ site.social.github }}" target="_blank" rel="noopener noreferrer" class="btn btn--secondary btn--sm">{{ channel.btn_text }}</a>
        {% elsif channel.type == "about" %}
          <span style="font-weight: 600; font-size: 0.95rem; color: var(--accent-emerald);">{{ channel.status_text }}</span>
          <a href="{{ '/about.html' | relative_url }}" class="btn btn--secondary btn--sm">{{ channel.btn_text }}</a>
        {% endif %}
      </div>
    </div>
  {% endfor %}

</div>
