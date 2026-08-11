---
layout: page
title: "Curriculum Vitae"
permalink: /cv.html
---

<!-- Print & Download Control row -->
<div class="no-print" style="display: flex; gap: 1rem; margin-bottom: 2.5rem; justify-content: flex-end; flex-wrap: wrap;">
  <a href="{{ '/assets/cv/cv.pdf' | relative_url }}" class="btn btn--accent" download style="padding: 0.5rem 1rem; font-size: 0.85rem;">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="vertical-align: middle;">
      <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
    </svg>
    Download PDF Resume
  </a>
  <button onclick="window.print()" class="btn btn--secondary" style="padding: 0.5rem 1rem; font-size: 0.85rem;">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="vertical-align: middle;">
      <path stroke-linecap="round" stroke-linejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
    </svg>
    Print CV
  </button>
</div>

<div class="cv-wrapper" style="font-size: 1rem; line-height: 1.5; color: var(--text-primary);">
  
  <!-- Header Info -->
  <div style="border-bottom: 2px solid var(--primary); padding-bottom: 1rem; margin-bottom: 2rem;">
    <h2 style="font-size: 2.2rem; margin-bottom: 0.25rem;">Kien Nguyen</h2>
    <p style="font-size: 1.15rem; font-weight: 600; color: var(--accent); margin-bottom: 0.5rem;">Senior DevOps / SRE / Cloud Engineer</p>
    <div style="font-size: 0.9rem; color: var(--text-muted); display: flex; flex-wrap: wrap; gap: 1rem;">
      <span><strong>Email:</strong> kien.nguyen@example.com</span>
      <span><strong>Location:</strong> Vietnam</span>
      <span><strong>GitHub:</strong> github.com/kiennt308</span>
      <span><strong>LinkedIn:</strong> linkedin.com/in/kiennt308</span>
    </div>
  </div>

  <!-- Professional Summary -->
  <div style="margin-bottom: 2rem;">
    <h3 style="font-size: 1.25rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--primary); border-bottom: 1px solid var(--border); padding-bottom: 0.25rem; margin-bottom: 0.75rem;">
      Professional Summary
    </h3>
    <p style="margin-bottom: 0;">
      Results-driven Senior DevOps and Cloud Engineer with over 6 years of experience designing, automating, and maintaining high-availability, cloud-native environments. Proven expertise in infrastructure-as-code (Terraform), container orchestration (Kubernetes), GitOps release management, and observability stacks. Adept at optimizing platform efficiency, securing architectures, and coordinating incident resolutions.
    </p>
  </div>

  <!-- Technical Competencies -->
  <div style="margin-bottom: 2rem;">
    <h3 style="font-size: 1.25rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--primary); border-bottom: 1px solid var(--border); padding-bottom: 0.25rem; margin-bottom: 0.75rem;">
      Technical Competencies
    </h3>
    <div style="display: grid; grid-template-columns: 1fr; gap: 0.5rem; font-size: 0.9rem;">
      <div><strong>Cloud Providers:</strong> Amazon Web Services (AWS), Azure, GCP</div>
      <div><strong>Container & Orchestration:</strong> Kubernetes, EKS, Docker, Helm, ArgoCD, Karpenter</div>
      <div><strong>Infrastructure as Code:</strong> Terraform, Terragrunt, Ansible, CloudFormation</div>
      <div><strong>CI/CD Pipelines:</strong> GitHub Actions, GitLab CI, Jenkins, GitOps</div>
      <div><strong>Observability:</strong> OpenTelemetry, Prometheus, Grafana, Loki, AWS CloudWatch</div>
      <div><strong>Languages & Shells:</strong> Python, Go, Bash, SQL, YAML</div>
      <div><strong>Operating Systems:</strong> Linux (Debian, RedHat, CentOS)</div>
    </div>
  </div>

  <!-- Professional Experience -->
  <div style="margin-bottom: 2rem;">
    <h3 style="font-size: 1.25rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--primary); border-bottom: 1px solid var(--border); padding-bottom: 0.25rem; margin-bottom: 1.25rem;">
      Professional Experience
    </h3>

    <!-- Job 1 -->
    <div style="margin-bottom: 1.5rem;">
      <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; margin-bottom: 0.25rem;">
        <h4 style="margin: 0; font-size: 1.1rem; color: var(--text-primary);">Senior DevOps / Cloud Engineer</h4>
        <span style="font-size: 0.85rem; font-weight: 600; color: var(--accent);">2024 – PRESENT</span>
      </div>
      <div style="font-size: 0.9rem; font-weight: 500; color: var(--text-muted); margin-bottom: 0.5rem;">Apex Scale Technologies</div>
      <ul style="margin-left: 1.25rem; font-size: 0.95rem; display: flex; flex-direction: column; gap: 0.35rem;">
        <li>Designed and configured secure AWS Multi-Account environments using AWS Control Tower and custom Terraform blueprints, resolving federated access and landing zones.</li>
        <li>Built GitOps-oriented delivery architectures with ArgoCD running on EKS, managing continuous releases for 120+ Microservices.</li>
        <li>Configured cluster compute node provisioning via Karpenter on AWS EKS, reducing overall cloud spend by 40%.</li>
        <li>Standardized OpenTelemetry distributed tracing and custom metrics across platforms, rendering them on Grafana.</li>
      </ul>
    </div>

    <!-- Job 2 -->
    <div style="margin-bottom: 1.5rem;">
      <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; margin-bottom: 0.25rem;">
        <h4 style="margin: 0; font-size: 1.1rem; color: var(--text-primary);">Cloud Engineer</h4>
        <span style="font-size: 0.85rem; font-weight: 600; color: var(--accent);">2023 – 2024</span>
      </div>
      <div style="font-size: 0.9rem; font-weight: 500; color: var(--text-muted); margin-bottom: 0.5rem;">CloudBound Solutions</div>
      <ul style="margin-left: 1.25rem; font-size: 0.95rem; display: flex; flex-direction: column; gap: 0.35rem;">
        <li>Managed and updated modular infrastructure files utilizing Terraform/Terragrunt for VPC, RDS, and S3 resources.</li>
        <li>Migrated deployment pipelines to GitHub Actions, accelerating release cycles by 35% with optimized runner caches.</li>
        <li>Applied container scanning integrations (Trivy, Snyk) inside build streams to secure artifact registry uploads.</li>
        <li>Set up alert parameters via Alertmanager, logging metrics to prevent service outages.</li>
      </ul>
    </div>

    <!-- Job 3 -->
    <div style="margin-bottom: 0;">
      <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; margin-bottom: 0.25rem;">
        <h4 style="margin: 0; font-size: 1.1rem; color: var(--text-primary);">System Administrator / Integration Engineer</h4>
        <span style="font-size: 0.85rem; font-weight: 600; color: var(--accent);">2020 – 2023</span>
      </div>
      <div style="font-size: 0.9rem; font-weight: 500; color: var(--text-muted); margin-bottom: 0.5rem;">Vanguard Systems Integrators</div>
      <ul style="margin-left: 1.25rem; font-size: 0.95rem; display: flex; flex-direction: column; gap: 0.35rem;">
        <li>Configured and resolved Linux and Windows host errors, maintaining a 99.9% application uptime rate.</li>
        <li>Wrote operational scripts (Python, Bash) to run DB backups, system health scans, and automate log rotation tasks.</li>
        <li>Administered network systems (DNS, Firewalls, VPN gateways, Active Directory) for enterprise clients.</li>
        <li>Conducted migration tasks, converting physical boxes to AWS EC2 architectures.</li>
      </ul>
    </div>

  </div>

  <!-- Education & Certs Split -->
  <div style="display: grid; grid-template-columns: 1fr; gap: 2rem; margin-bottom: 2rem; page-break-inside: avoid;">
    
    <!-- Education -->
    <div>
      <h3 style="font-size: 1.25rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--primary); border-bottom: 1px solid var(--border); padding-bottom: 0.25rem; margin-bottom: 0.75rem;">
        Education
      </h3>
      <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap;">
        <strong>B.S. in Computer Science / Engineering</strong>
        <span style="font-size: 0.85rem; font-weight: 600; color: var(--accent);">2016 – 2020</span>
      </div>
      <div style="font-size: 0.9rem; color: var(--text-secondary);">Vietnam National University</div>
    </div>

    <!-- Key Certifications -->
    <div>
      <h3 style="font-size: 1.25rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--primary); border-bottom: 1px solid var(--border); padding-bottom: 0.25rem; margin-bottom: 0.75rem;">
        Certifications
      </h3>
      <div style="font-size: 0.95rem; display: grid; grid-template-columns: 1fr; gap: 0.25rem;">
        <span>AWS Certified Solutions Architect – Professional (2025)</span>
        <span>AWS Certified DevOps Engineer – Professional (2025)</span>
        <span>Certified Kubernetes Administrator (CKA, 2024)</span>
        <span>Certified Kubernetes Security Specialist (CKS, 2024)</span>
      </div>
    </div>
  </div>

  <!-- Research & Publications -->
  <div style="page-break-inside: avoid;">
    <h3 style="font-size: 1.25rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--primary); border-bottom: 1px solid var(--border); padding-bottom: 0.25rem; margin-bottom: 0.75rem;">
      Academic Research & Publications
    </h3>
    <ul style="margin-left: 1.25rem; font-size: 0.95rem; display: flex; flex-direction: column; gap: 0.35rem;">
      <li><strong>Publication:</strong> <em>"Attention-Based Spatial-Temporal Fusion for EEG-Based Emotion Recognition"</em> - International Joint Conference on Neural Networks (IJCNN 2025).</li>
      <li><strong>Pre-print:</strong> <em>"Multimodal Emotion Classification Using Deep Transformer Networks and Physiological Signals"</em> - Under Review, IEEE Transactions on Affective Computing (2026).</li>
    </ul>
  </div>

</div>
