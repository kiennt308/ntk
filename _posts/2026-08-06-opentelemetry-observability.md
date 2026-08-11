---
layout: post
title: "Building an Observability Platform with OpenTelemetry"
description: "A practical guide to building an enterprise-grade observability platform using the OpenTelemetry Collector, Prometheus, Loki, and Grafana."
date: 2026-08-06 13:00:00 +0700
categories: [Observability]
tags: [OpenTelemetry, Observability, Grafana, Prometheus, SRE]
---

In modern distributed microservice systems, understanding *why* a transaction failed or *where* latency is occurring is a massive challenge. Traditional monitoring is no longer sufficient. We need **Observability**—the ability to infer the internal state of a system based on its external outputs: Metrics, Logs, and Traces.

OpenTelemetry (OTel) has emerged as the CNCF standard for generating, collecting, and exporting telemetry data. In this guide, we'll configure an OpenTelemetry collector pipeline to gather logs, metrics, and traces and forward them to Prometheus, Loki, and Grafana.

---

## 1. The Three Pillars of Telemetry

* **Metrics (Is there a problem?):** Numeric values measured over time (e.g., CPU utilization, HTTP request rates).
* **Logs (What happened?):** Structured text records generated when events occur (e.g., application stack traces, auth failures).
* **Traces (Where is the bottleneck?):** The path of a request as it travels through multiple microservices, detailing latency timings for each step (spans).

---

## 2. OpenTelemetry Collector Architecture

The **OpenTelemetry Collector** is a proxy agent that receives telemetry data, processes it (filtering, batching, scrubbing credentials), and exports it to databases.

```text
[Applications / Pods]
        │ (OTLP protocol)
        ▼
┌────────────────────────────────────────────────────────┐
│               OpenTelemetry Collector                  │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────┐  │
│  │  Receivers   │ ─►│  Processors  │ ─►│ Exporters  │  │
│  └──────────────┘   └──────────────┘   └────────────┘  │
└────────────────────────────────────────────────────────┘
                                               │
               ┌───────────────────────────────┼──────────────────────────────┐
               ▼ (OTLP / Prometheus)           ▼ (OTLP / Jaeger)              ▼ (Loki API)
         [ Prometheus / Mimir ]                   [ Tempo / Jaeger ]             [ Loki ]
```

---

## 3. Configuring the OpenTelemetry Collector

Below is a complete, production-ready configuration YAML file for the OpenTelemetry Collector. It defines receivers for OTLP (gRPC and HTTP), batching processors, and exporters to forward data to Prometheus, Grafana Tempo, and Loki:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  # Batch data together to optimize networks and database insert writes
  batch:
    send_batch_size: 8192
    timeout: 5s
    send_batch_max_size: 10240

  # Memory limiter to prevent collector crashes under heavy traffic spikes
  memory_limiter:
    check_interval: 1s
    limit_percentage: 80
    spike_limit_percentage: 20

exporters:
  # Export metrics in Prometheus format
  prometheus:
    endpoint: "0.0.0.0:8889"
    namespace: "otel"

  # Export traces to Grafana Tempo / Jaeger via OTLP gRPC
  otlp/tempo:
    endpoint: "tempo-collector.monitoring.svc.cluster.local:4317"
    tls:
      insecure: true

  # Export logs to Grafana Loki
  loki:
    endpoint: "http://loki.monitoring.svc.cluster.local:3100/loki/api/v1/push"

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [prometheus]
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp/tempo]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [loki]

  telemetry:
    logs:
      level: "info"
```

---

## 4. Correlating Telemetry in Grafana

The true power of OpenTelemetry is **correlation**. When you view a dashboard in Grafana, OTel allows you to click on a spike in your HTTP latency metric and instantly view the corresponding distributed traces during that exact time window. From the trace page, you can drill down into the logs of the specific container that failed.

This connection is achieved by injecting `trace_id` and `span_id` headers into application logs and passing context across service calls via HTTP carrier headers (W3C Trace Context).

---

## 5. Summary

Building a unified observability pipeline prevents vendor lock-in and reduces developer overhead. By leveraging OpenTelemetry SDKs inside application code and deploying the OTel Collector to manage the batching and routing, you establish a highly scalable, real-time diagnostic system across your platform.
