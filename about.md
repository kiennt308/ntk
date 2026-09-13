---
layout: page
title: "About Kien Nguyen"
permalink: /about.html
---

<div class="about-hero-card" style="display: flex; gap: 2rem; align-items: center; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 2.25rem; box-shadow: var(--shadow-sm); margin-bottom: 3rem; flex-wrap: wrap;">
  <div class="author-avatar" style="width: 88px; height: 88px; font-size: 2rem; border-radius: var(--radius-lg);">
    KN
  </div>
  <div style="flex: 1; min-width: 280px;">
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem; flex-wrap: wrap;">
      <h2 style="font-size: 1.85rem; margin: 0; color: var(--text-primary);">Kien Nguyen</h2>
      <span class="badge badge--primary">Senior DevOps / SRE</span>
    </div>
    <div style="font-size: 0.95rem; color: var(--accent-primary); font-weight: 600; margin-bottom: 0.65rem;">
      Cloud Architect & Platform Engineer
    </div>
    <div style="font-size: 0.875rem; color: var(--text-muted); display: flex; flex-wrap: wrap; gap: 1.25rem;">
      <span>📍 Vietnam</span>
      <span>✉️ <a href="mailto:{{ site.email }}" style="color: inherit;">{{ site.email }}</a></span>
      <span>🐙 <a href="https://github.com/{{ site.social.github }}" target="_blank" rel="noopener noreferrer" style="color: inherit;">github.com/{{ site.social.github }}</a></span>
      <span>💼 <a href="https://linkedin.com/in/{{ site.social.linkedin }}" target="_blank" rel="noopener noreferrer" style="color: inherit;">linkedin.com/in/{{ site.social.linkedin }}</a></span>
    </div>
  </div>
</div>

## 1. Background & Engineering Philosophy

I am a **Senior DevOps, SRE, and Cloud Architect** with over 6 years of experience designing, automating, and maintaining high-availability, cloud-native infrastructures. My practice centers around treating infrastructure as versioned software, building self-healing Kubernetes platforms, and implementing robust end-to-end observability systems.

### Core Areas of Focus
* **☁️ Cloud Architecture:** Multi-region, multi-account AWS landing zones utilizing AWS Control Tower, transit networking, and strict security guardrails.
* **🚢 Platform Engineering:** Standardizing developer environments, internal developer portals, and ArgoCD GitOps pipelines to accelerate delivery cycles.
* **📊 Site Reliability Engineering:** Software-driven operations, SLO/SLA management, automated incident triage, and blameless postmortem culture.

### Engineering Principles
* **Automate Everything:** If an operational task needs to be performed more than twice, it deserves a tested script or pipeline.
* **Simplicity by Design:** Complex, fragile pipelines break easily. Build modular, observable, and resilient architectures.
* **Documentation is Code:** Systems that are not documented do not exist. Clear runbooks and architecture decision records (ADRs) are essential.
* **Security & Least Privilege:** Implement zero-trust network boundaries, automated container scanning, and continuous compliance guardrails.

---

## 2. Technical Competencies Matrix

<div class="grid grid--2col" style="gap: 1.25rem; margin: 2rem 0;">
  <div class="card" style="padding: 1.5rem;">
    <h4 style="margin: 0 0 0.75rem 0; font-size: 1.05rem; color: var(--accent-primary);">☁️ Cloud & Infrastructure</h4>
    <p style="font-size: 0.925rem; margin-bottom: 0; color: var(--text-secondary);">
      AWS (Control Tower, Organizations, VPC, IAM, Transit Gateway, Route53), GCP, Microsoft Azure.
    </p>
  </div>

  <div class="card" style="padding: 1.5rem;">
    <h4 style="margin: 0 0 0.75rem 0; font-size: 1.05rem; color: var(--accent-cyan);">🚢 Containers & Orchestration</h4>
    <p style="font-size: 0.925rem; margin-bottom: 0; color: var(--text-secondary);">
      Kubernetes, Amazon EKS, Docker, Helm, ArgoCD, Karpenter, Cilium CNI, Istio Service Mesh.
    </p>
  </div>

  <div class="card" style="padding: 1.5rem;">
    <h4 style="margin: 0 0 0.75rem 0; font-size: 1.05rem; color: var(--accent-primary);">🏗️ Infrastructure as Code</h4>
    <p style="font-size: 0.925rem; margin-bottom: 0; color: var(--text-secondary);">
      Terraform, Terragrunt, OpenTofu, Ansible, AWS CloudFormation, Policy-as-Code (OPA).
    </p>
  </div>

  <div class="card" style="padding: 1.5rem;">
    <h4 style="margin: 0 0 0.75rem 0; font-size: 1.05rem; color: var(--accent-emerald);">📊 Observability & SRE</h4>
    <p style="font-size: 0.925rem; margin-bottom: 0; color: var(--text-secondary);">
      OpenTelemetry Collector, Prometheus, Grafana, Loki, Alertmanager, AWS CloudWatch.
    </p>
  </div>

  <div class="card" style="padding: 1.5rem;">
    <h4 style="margin: 0 0 0.75rem 0; font-size: 1.05rem; color: var(--accent-rose);">⚡ CI/CD & DevSecOps</h4>
    <p style="font-size: 0.925rem; margin-bottom: 0; color: var(--text-secondary);">
      GitHub Actions, GitLab CI, Jenkins, Trivy, Snyk, SonarQube, Cosign.
    </p>
  </div>

  <div class="card" style="padding: 1.5rem;">
    <h4 style="margin: 0 0 0.75rem 0; font-size: 1.05rem; color: var(--accent-amber);">💻 Languages & Operating Systems</h4>
    <p style="font-size: 0.925rem; margin-bottom: 0; color: var(--text-secondary);">
      Python, Go, Bash Shell Scripting, SQL, Linux (Ubuntu, Debian, RHEL, Amazon Linux).
    </p>
  </div>
</div>

---

## 3. Professional Work Experience

<div class="timeline-wrapper" style="display: flex; flex-direction: column; gap: 2rem; margin: 2rem 0;">

  <!-- Job 1 -->
  <div class="card" style="padding: 1.75rem 2rem;">
    <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; margin-bottom: 0.25rem;">
      <h3 style="margin: 0; font-size: 1.25rem; color: var(--text-primary);">Senior DevOps / Cloud Engineer</h3>
      <span class="badge badge--amber">2024 – PRESENT</span>
    </div>
    <div style="font-size: 0.95rem; font-weight: 600; color: var(--accent-primary); margin-bottom: 1rem;">Apex Scale Technologies</div>
    <ul style="margin-left: 1.25rem; font-size: 0.95rem; display: flex; flex-direction: column; gap: 0.5rem; color: var(--text-secondary);">
      <li>Designed and configured enterprise AWS Multi-Account environments using AWS Control Tower and custom modular Terraform blueprints.</li>
      <li>Built GitOps delivery workflows with ArgoCD on EKS, managing continuous zero-downtime releases for 120+ Microservices.</li>
      <li>Configured dynamic cluster node autoscaling with Karpenter on AWS EKS, reducing overall compute spend by 40%.</li>
      <li>Standardized OpenTelemetry distributed tracing and metrics aggregation across distributed services, visualized in Grafana dashboards.</li>
    </ul>
  </div>

  <!-- Job 2 -->
  <div class="card" style="padding: 1.75rem 2rem;">
    <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; margin-bottom: 0.25rem;">
      <h3 style="margin: 0; font-size: 1.25rem; color: var(--text-primary);">Cloud Engineer</h3>
      <span class="badge badge--primary">2023 – 2024</span>
    </div>
    <div style="font-size: 0.95rem; font-weight: 600; color: var(--accent-primary); margin-bottom: 1rem;">CloudBound Solutions</div>
    <ul style="margin-left: 1.25rem; font-size: 0.95rem; display: flex; flex-direction: column; gap: 0.5rem; color: var(--text-secondary);">
      <li>Managed and deployed modular infrastructure utilizing Terraform & Terragrunt for VPC, EKS, RDS, and S3 resources.</li>
      <li>Migrated CI/CD pipelines to GitHub Actions, accelerating release velocity by 35% using optimized runner caches.</li>
      <li>Integrated automated container security vulnerability scanning (Trivy, Snyk) within delivery pipelines.</li>
      <li>Configured Alertmanager routing and structured log aggregation to reduce Mean Time to Detection (MTTD).</li>
    </ul>
  </div>

  <!-- Job 3 -->
  <div class="card" style="padding: 1.75rem 2rem;">
    <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; margin-bottom: 0.25rem;">
      <h3 style="margin: 0; font-size: 1.25rem; color: var(--text-primary);">System Administrator & Infrastructure Engineer</h3>
      <span class="badge badge--cyan">2020 – 2023</span>
    </div>
    <div style="font-size: 0.95rem; font-weight: 600; color: var(--accent-primary); margin-bottom: 1rem;">Vanguard Systems Integrators</div>
    <ul style="margin-left: 1.25rem; font-size: 0.95rem; display: flex; flex-direction: column; gap: 0.5rem; color: var(--text-secondary);">
      <li>Administered production Linux host environments and internal networking, achieving 99.9% service uptime.</li>
      <li>Authored automated maintenance scripts in Python and Bash for database backups, health telemetry, and log rotation.</li>
      <li>Planned and executed physical-to-cloud server migration procedures onto AWS EC2 instances.</li>
    </ul>
  </div>

</div>

---

## 4. Education, Certifications & Research

<div class="grid grid--2col" style="gap: 1.5rem; margin: 2rem 0;">
  
  <div class="card" style="padding: 1.75rem;">
    <h3 style="margin-top: 0; font-size: 1.2rem; color: var(--text-primary); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
      🎓 Education & Degrees
    </h3>
    <div style="margin-top: 1rem;">
      <strong>B.S. in Computer Science / Engineering</strong>
      <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.25rem;">Vietnam National University (2016 – 2020)</div>
      <p style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0;">
        Focus on distributed systems, operating systems internals, and network protocols.
      </p>
    </div>
  </div>

  <div class="card" style="padding: 1.75rem;">
    <h3 style="margin-top: 0; font-size: 1.2rem; color: var(--text-primary); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
      🏆 Professional Certifications
    </h3>
    <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.9rem;">
      <div>✓ <strong>AWS Solutions Architect – Professional</strong> (2025)</div>
      <div>✓ <strong>AWS DevOps Engineer – Professional</strong> (2025)</div>
      <div>✓ <strong>Certified Kubernetes Administrator (CKA)</strong> (2024)</div>
      <div>✓ <strong>Certified Kubernetes Security Specialist (CKS)</strong> (2024)</div>
    </div>
  </div>

</div>

### Academic Research & Publications
* 📄 **IJCNN 2025:** *"Attention-Based Spatial-Temporal Fusion for EEG-Based Emotion Recognition"* — International Joint Conference on Neural Networks.
* 📄 **IEEE Transactions (2026):** *"Multimodal Emotion Classification Using Deep Transformer Networks and Physiological Signals"* — Under Review.

---

<!-- Download Resume & Call to Action Box (Placed at the end after reading) -->
<div id="resume-download" class="card" style="margin-top: 3.5rem; padding: 2.5rem; text-align: center; background: linear-gradient(135deg, var(--bg-surface), var(--bg-subtle)); border: 1px solid rgba(var(--accent-primary-rgb), 0.35); box-shadow: var(--shadow-lg);">
  <div style="font-size: 2.25rem; margin-bottom: 0.5rem;">📄</div>
  <h2 style="font-size: 1.85rem; margin-top: 0; margin-bottom: 0.5rem;">Curriculum Vitae / Resume</h2>
  <p style="color: var(--text-secondary); max-width: 580px; margin: 0 auto 1.75rem auto; font-size: 1.05rem;">
    Looking for a comprehensive breakdown of technical milestones, project architectures, and references? Download the complete PDF resume below.
  </p>

  <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1.5rem;">
    <a href="{{ '/assets/cv/cv.pdf' | relative_url }}" class="btn btn--accent" download style="padding: 0.75rem 1.75rem; font-size: 1rem;">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
      </svg>
      Download PDF Resume
    </a>

    <button onclick="window.print()" class="btn btn--secondary" style="padding: 0.75rem 1.5rem; font-size: 1rem;">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
      </svg>
      Print Resume
    </button>
  </div>

  <div style="font-size: 0.9rem; color: var(--text-muted);">
    Interested in collaborating or consulting? <a href="{{ '/contact.html' | relative_url }}" style="font-weight: 600;">Get in touch →</a>
  </div>
</div>
