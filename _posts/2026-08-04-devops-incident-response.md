---
layout: post
title: "DevOps Incident Response: From Alert to Postmortem"
description: "A playbook for handling high-priority production incidents, covering alerting, triage, hot mitigation, and writing blameless postmortems."
date: 2026-08-04 15:00:00 +0700
categories: [DevOps]
tags: [SRE, Incident Response, Postmortem, Monitoring]
---

In modern operations, outages are an inevitable reality of running systems at scale. No matter how many redundant regions you deploy, software will crash, configurations will drift, and cloud providers will experience underlying hardware failures.

How your engineering organization responds to these failures is what separates elite SRE teams from the rest. In this playbook, we'll map the incident lifecycle from the initial alert trigger down to the blameless postmortem.

---

## 1. The Incident Response Lifecycle

```text
  [Alert Triggered]
         │
         ▼
    [Triage] ──────► [Mitigation] ──────► [Resolution] ──────► [Postmortem]
(Assess severity)    (Stop the bleeding)    (Root cause fix)    (Prevent repeat)
```

---

## 2. Setting Up Actionable Alerting

An incident begins with detection. To keep your team alert and prevent alarm fatigue, you must separate **Alerts** from **Tickets**:

* **Actionable Alerts (Paging):** Triggered when a system boundary is violated that requires immediate human intervention (e.g., HTTP 5xx rates above 5%, payment gateway timeouts). Pagers sound immediately.
* **Non-Actionable Events (Tickets):** Triggered when a threshold is crossed but the system is self-healing or can wait until business hours (e.g., single node CPU spikes to 95%, disk space reaches 80%). These write Jira tickets, not pager alerts.

Here is a Prometheus alerting rule configuration sample:

{% raw %}
```yaml
groups:
- name: payment-gateway-alerts
  rules:
  - alert: HighPaymentFailureRate
    expr: sum(rate(http_requests_total{status=~"5..", path="/pay"}[5m])) / sum(rate(http_requests_total{path="/pay"}[5m])) * 100 > 5
    for: 2m
    labels:
      severity: critical
      tier: api
    annotations:
      summary: "High payment failure rates detected: {{ $value | printf \"%.2f\" }}%"
      runbook_url: "https://wiki.internal/sre/runbooks/payments-failure"
```
{% endraw %}

---

## 3. Incident Triage and Mitigation Under Pressure

When you receive a critical alert, your goal is **mitigation**, not deep-dive debugging. *Stop the bleeding first.*

1. **Acknowledge the Alert:** Mark the incident as acknowledged in PagerDuty/Opsgenie so the backup rotation is not paged.
2. **Open a War Room:** Create a dedicated Zoom link and Slack channel (`#incident-2026-08-04-pay-error`).
3. **Declare Roles:** Assign an **Incident Commander** (facilitates communications and delegates tasks) and a **Lead Engineer** (performs technical diagnosis).
4. **Identify the Last Change:** 80% of outages are caused by recent deployments or configuration changes. Check the CI/CD pipeline history immediately.
5. **Apply Mitigation:** Roll back the last deployment, scale up the replicas, or isolate traffic. Do not write hotfixes under pressure unless a rollback is impossible.

---

## 4. Writing a Blameless Postmortem

Once the incident is resolved, schedule a postmortem review within 48 hours. The meeting must be **blameless**. If engineers fear punishment for mistakes, they will hide details, making it impossible to address systemic issues.

### The Five Whys Technique
To find the root cause, ask "Why?" recursively:
1. *Why did the database crash?* Because it ran out of memory.
2. *Why did it run out of memory?* Because a query retrieved too many records.
3. *Why did the query retrieve too many records?* Because the database index was dropped.
4. *Why was the index dropped?* Because a migration script was run with an incorrect parameter.
5. *Why was it run with an incorrect parameter?* Because migration scripts are run manually from dev machines instead of inside an automated pipeline.

---

## 5. Postmortem Template Outline

```markdown
# Incident Postmortem: [YYYY-MM-DD] - [Brief Summary]

## Executive Summary
* **Severity:** P1 (Critical)
* **Duration:** 42 minutes (14:10 UTC to 14:52 UTC)
* **Impact:** 12% of customer checkout attempts failed with HTTP 500 errors.

## Timeline
* **14:10** - Alert HighPaymentFailureRate fires in Slack/PagerDuty.
* **14:12** - Incident Commander acknowledges and opens #incident channel.
* **14:22** - Identified recent database migration script run by developer.
* **14:35** - Re-applied missing index manually to production DB.
* **14:52** - Payment success rates return to baseline. Alert resolves.

## Action Items
1. [ ] Automate database migration dry-runs in CI/CD pipeline.
2. [ ] Add index verification check prior to schema executions.
3. [ ] Set up database CPU/Memory alerts in Datadog.
```

---

## 6. Summary

ELite operational stability is not achieved by hoping systems never break. It is built through clear, noise-reduced monitoring, structured triage execution patterns, and a blameless engineering culture that treats every outage as a free training session to improve platform resiliency.
