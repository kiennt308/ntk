---
layout: post
title: "How I Design a Production-Ready AWS Environment"
description: "A comprehensive guide to planning and deploying a production-ready AWS environment using modular Terraform, multi-AZ VPC topologies, and secure transit networking."
date: 2026-08-09 10:00:00 +0700
categories: [AWS]
tags: [AWS, Terraform, Networking, Security, Cloud Architecture]
---

Designing a production environment on AWS is about balancing cost, redundancy, security, and developer ergonomics. A poorly planned network topology or account structure can cost tens of thousands of dollars in NAT Gateway fees and introduce major security vectors.

In this guide, we'll design a standard, production-ready AWS foundation utilizing VPC best practices, multi-AZ high availability, and Infrastructure as Code.

---

## 1. VPC Subnet Allocation Model

For a highly available production workload, we spread resources across three Availability Zones (AZs). In each AZ, we allocate three distinct subnet tiers:

1. **Public Subnet:** Houses internet-facing resources like ALBs and NAT Gateways.
2. **Private App Subnet:** Houses application runtimes (Kubernetes nodes, ECS tasks, EC2 instances). No public IPs are allowed here.
3. **Private Database Subnet:** Houses databases (RDS, Elasticache). Highly isolated, only accessible from the private app tier.

```text
Availability Zone A          Availability Zone B          Availability Zone C
├── Public Subnet (1A)       ├── Public Subnet (1B)       ├── Public Subnet (1C)
├── Private App Subnet (2A)  ├── Private App Subnet (2B)  ├── Private App Subnet (2C)
└── Private DB Subnet (3A)   └── Private DB Subnet (3B)   └── Private DB Subnet (3C)
```

---

## 2. NAT Gateway Topologies: Cost vs Redundancy

A common point of failure—and cost surprise—is the **NAT Gateway**. Traffic from private subnets heading out to the internet (e.g., downloading npm packages or calling public APIs) must go through a NAT Gateway.

You have two design patterns:
* **Single NAT Gateway:** Best for staging or non-production. All private traffic goes through one gateway in AZ-A. If AZ-A fails, private subnets lose internet access.
* **Multi-AZ NAT Gateways:** Standard for production. You deploy one NAT Gateway per AZ. This ensures AZ-level isolation but triples your baseline hourly NAT fees.

---

## 3. Terraform Infrastructure Configuration

Writing this using Terraform allows you to maintain consistency across multiple environments. Below is a production-ready Terraform VPC module example using the official community VPC module:

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "production-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  database_subnets = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]

  create_database_subnet_group = true

  # Deploy one NAT Gateway per Availability Zone for high availability
  enable_nat_gateway     = true
  single_nat_gateway     = false
  one_nat_gateway_per_az = true

  enable_dns_hostnames = true
  enable_dns_support   = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
  }
}
```

---

## 4. Key Security Implementations

### VPC Flow Logs
Always enable VPC Flow Logs. Stream them to a centralized S3 bucket or CloudWatch Log Group for auditing network rejects:

```hcl
resource "aws_flow_log" "vpc_flow_logs" {
  iam_role_arn    = aws_iam_role.flow_logs_role.arn
  log_destination = aws_cloudwatch_log_group.flow_logs.arn
  traffic_type    = "ALL"
  vpc_id          = module.vpc.vpc_id
}
```

### NACLs (Network Access Control Lists)
Use NACLs as stateless secondary firewalls. For database subnets, restrict inbound traffic strictly to the CIDR blocks of your private app subnets, blocking any outside interaction.

---

## 5. Transit Gateway: Connecting Accounts

If you are operating a multi-account organization, do not use VPC peering between dozens of accounts. Instead, use an **AWS Transit Gateway (TGW)**. 

TGW acts as a cloud router. Each VPC attaches to the Transit Gateway, and route tables inside TGW control which VPCs can talk to each other (e.g., preventing a staging VPC from reaching a production database VPC).

---

## 6. Summary

Building a production-ready AWS environment requires establishing secure boundaries before launching compute instances. By mapping multi-AZ subnet hierarchies, provisioning redundant NAT Gateways, and documenting everything in Terraform, you create a stable foundation that is audit-compliant and ready to host container platforms like EKS.
