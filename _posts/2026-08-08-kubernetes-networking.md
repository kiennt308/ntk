---
layout: post
title: "Kubernetes Networking Explained"
description: "Demystifying the Kubernetes networking model, covering Pod-to-Pod communication, the role of kube-proxy, CoreDNS service resolution, and Ingress routing."
date: 2026-08-08 11:00:00 +0700
categories: [Kubernetes]
tags: [Kubernetes, Networking, Pod, Service, Ingress]
---

Kubernetes networking is often considered one of the most complex components of container orchestration. It requires coordinating virtual network interfaces, routing tables, DNS resolution, and packet filtering across a cluster of bare-metal or virtual nodes.

In this guide, we'll break down the fundamental rules of Kubernetes networking and walk through how packets travel from a user's browser down to a pod.

---

## 1. The Core Networking Model

Kubernetes imposes one fundamental rule: **Every Pod gets its own unique, routable IP address.**

This model avoids the need for dynamic port mappings (like you might have seen in standard Docker host modes). A Pod can communicate with any other Pod on any node without NAT, treating the cluster as a flat local network.

This flat structure is managed by a **CNI (Container Network Interface)** plugin. CNIs generally fall into two categories:

* **Overlay Networks (e.g., Calico, Flannel):** Create a virtual network on top of the host network. Packets are encapsulated (using VXLAN or Geneve) inside standard host packets and decrypted on the receiving node. This introduces minor CPU overhead but works on any cloud.
* **Underlay Networks (e.g., AWS VPC CNI):** Allocate real IPs from the underlying cloud VPC network directly to Pods. Packets are routed using the native cloud router, resulting in bare-metal speeds and no encapsulation overhead.

---

## 2. Pod-to-Pod Communication

When Pod A on Node 1 wants to send a packet to Pod B on Node 2:

1. Pod A sends a packet destined for Pod B's IP.
2. The packet leaves Pod A's network namespace via a virtual ethernet pair (`veth`) connected to the node's bridge interface.
3. The node's kernel checks the routing table.
4. If using an overlay CNI, the packet is wrapped in a host packet and routed to Node 2.
5. Node 2's kernel unwraps the packet and forwards it to Pod B's virtual interface.

---

## 3. Pod-to-Service: Kube-Proxy & iptables

Pods are ephemeral; they are terminated and replaced constantly, changing their IPs. To solve this, Kubernetes uses **Services** which provide a single, stable IP address (ClusterIP) that routes traffic to a set of backend Pods.

But a Service IP is virtual—no physical interface or device owns it. Instead, **kube-proxy** (running on every node) configures network rules to intercept traffic destined for Service IPs.

kube-proxy operates in two main modes:
* **iptables mode (default):** Configures Linux kernel iptables rules to randomly distribute connections across backend Pods. While stable, large clusters with thousands of services suffer performance degradation as iptables is evaluated sequentially.
* **IPVS (IP Virtual Server) mode:** Uses Netfilter's IPVS hash tables, routing packets in constant time $\mathcal{O}(1)$. Highly recommended for enterprise scale.

---

## 4. Ingress: Routing External Traffic

To expose services to the outside world, you use an **Ingress Controller** (e.g., NGINX Ingress, AWS Load Balancer Controller). The Ingress Controller runs as a Pod inside the cluster, exposed via a LoadBalancer service, and translates Kubernetes Ingress manifests into routing configurations.

Here is a standard Kubernetes Ingress manifest routing traffic to a frontend service:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-frontend-service
            port:
              number: 80
```

When a request hits `app.example.com`:
1. The DNS routes the connection to the external Load Balancer.
2. The Load Balancer forwards the packet to the NGINX Ingress Controller Pods.
3. NGINX inspects the Host header and path, then forwards the packet directly to the backend Pod IPs (bypassing the Service IP to optimize hop counts).

---

## 5. CoreDNS: Service Discovery

Every time you deploy a service, Kubernetes automatically registers a DNS entry in the cluster's internal DNS server (**CoreDNS**). 

For example, a Pod in the same namespace can call another service using its short name:

```bash
curl http://web-frontend-service
```

CoreDNS resolves this query to the virtual ClusterIP of the service, which is then routed by kube-proxy's iptables rules to the target containers.

---

## 6. Summary

Kubernetes networking coordinates multiple layers—from container network namespaces and CNI overlay routing down to kernel-level iptables load balancing and DNS registries. Understanding how these pieces align is essential for troubleshooting connection dropouts, latency spikes, and building secure service boundaries.
