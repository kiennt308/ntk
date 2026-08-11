---
layout: post
title: "AWS EKS Production Checklist"
description: "A comprehensive security, networking, and scaling checklist for deploying enterprise workloads to Amazon Elastic Kubernetes Service (EKS)."
date: 2026-08-05 14:00:00 +0700
categories: [Kubernetes]
tags: [Kubernetes, EKS, Security, Production, AWS]
---

Amazon Elastic Kubernetes Service (EKS) handles the control plane setup, high availability, and patching of Kubernetes masters. However, out of the box, EKS defaults are not designed for enterprise production security or performance.

Before launching workloads in production, review this EKS production checklist spanning security, networking, storage, and node autoscaling.

---

## 1. Security Checklist

### Disable Public API Endpoint Access
By default, the EKS cluster endpoint is accessible from the internet. In production, restrict access:
* **Private access only:** Direct API communication goes through your VPC/VPN tunnels.
* **Public with CIDR restrictions:** If you must keep it public, white-list only your corporate VPN IPs.

### Enable IAM Roles for Service Accounts (IRSA)
Do not assign administrative IAM policies to the EC2 instances running your worker nodes. If a container is compromised, the attacker inherits access to your entire AWS account. Instead, use IRSA to bind IAM roles to specific Kubernetes ServiceAccounts.

Here is a Terraform block mapping an IAM OIDC Provider for EKS:

```hcl
data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.eks.url, "https://", "")}:sub"
      values   = ["system:serviceaccount:default:my-app-sa"]
    }

    principals {
      identifiers = [aws_iam_openid_connect_provider.eks.arn]
      type        = "Federated"
    }
  }
}

resource "aws_iam_role" "app_role" {
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
  name               = "eks-app-role"
}
```

---

## 2. Networking Checklist

### Prevent IP Exhaustion (AWS VPC CNI prefix delegation)
By default, the AWS VPC CNI assigns one secondary private IP to each Pod from the node's subnet. Small EC2 instance types have strict limits on the number of ENIs (Elastic Network Interfaces) they can attach, restricting you to as few as 4-8 pods per node regardless of remaining CPU/RAM.

Enable **Prefix Delegation** to allocate `/28` CIDR blocks (16 IPs) to each slot, increasing pod density:

```bash
kubectl set env daemonset/aws-node -n kube-system ENABLE_PREFIX_DELEGATION=true
```

### Configure Network Policies
The standard VPC CNI allows all pods to talk to all other pods. Apply **NetworkPolicies** (using Calico or native Amazon VPC CNI Network Policy features) to restrict namespace traffic (e.g., blocking the web-app frontend namespace from hitting the database namespace directly).

---

## 3. Storage Checklist

### Deploy Amazon EBS CSI Driver
EKS no longer includes in-tree EBS storage provisioners by default. You must install the EBS CSI Driver Helm Chart and provision an IAM service account role to allow the controller to provision EBS volumes dynamically.

### StorageClass Configuration
Configure your `StorageClass` with `volumeBindingMode: WaitForFirstConsumer` to ensure volumes are provisioned in the specific Availability Zone where the scheduler places the target Pod.

---

## 4. Scaling Checklist: Karpenter vs Cluster Autoscaler

For production, replace the legacy **Cluster Autoscaler** with **Karpenter**.

* **Cluster Autoscaler:** Relies on AWS Auto Scaling Groups (ASGs). When a pod is unschedulable, it increases the ASG size, taking 3–5 minutes to add nodes of a fixed size.
* **Karpenter:** Bypasses ASGs entirely. It talks directly to the EC2 Fleet APIs. It evaluates the CPU/RAM requests of pending pods and launches the optimal instance type within seconds, optimizing compute costs.

---

## 5. EKS Production Summary Checklist

| Category | Requirement | Verified |
| :--- | :--- | :---: |
| Security | Control Plane logging enabled (Authenticator, ControllerManager) | [ ] |
| Security | Secrets encryption enabled via AWS KMS CMK | [ ] |
| Networking | CoreDNS scaled via Cluster Proportional Autoscaler | [ ] |
| Cost | Node pools configured with Spot instances for non-critical pods | [ ] |
| Governance| Kyverno or Gatekeeper deployed to block unprivileged container runs | [ ] |

---

## 6. Summary

By securing your EKS control plane network, routing pod IAM access dynamically via IRSA federated providers, enabling CNI prefix delegation to maximize IP pools, and routing compute scale via Karpenter, you transition a default EKS cluster into a robust, secure, and production-ready host for cloud-native applications.
