---
document_id: DOC-INVENTORY-004
title: Inventory Service Operations and Troubleshooting Guide
document_type: troubleshooting
service: inventory-service
version: 2.9.1
product: nexora-commerce
created_at: 2025-01-10
updated_at: 2026-03-20
environment: [staging, production]
tags: [inventory-service, troubleshooting, INV-409]
severity: 
---

# Inventory Service Operations and Troubleshooting Guide

## Scope

This guide is the current operating reference owned by Supply Platform. It covers versions 2.8, 2.9, 2.9.1 and dependencies PostgreSQL 16, Kafka, Redis.

## Triage

The triage objective for inventory-service 2.9.1 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats INV-409 as the primary worked example while cross-checking INV-409, INV-503, KAFKA-302. Operators correlate gateway request IDs with inventory-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For INV-409, the catalog definition is: inventory-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Diagnosis

The diagnosis objective for inventory-service 2.9.1 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats INV-409 as the primary worked example while cross-checking INV-409, INV-503, KAFKA-302. Operators correlate gateway request IDs with inventory-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For INV-409, the catalog definition is: inventory-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Containment

The containment objective for inventory-service 2.9.1 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats INV-409 as the primary worked example while cross-checking INV-409, INV-503, KAFKA-302. Operators correlate gateway request IDs with inventory-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For INV-409, the catalog definition is: inventory-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Recovery

The recovery objective for inventory-service 2.9.1 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats INV-409 as the primary worked example while cross-checking INV-409, INV-503, KAFKA-302. Operators correlate gateway request IDs with inventory-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For INV-409, the catalog definition is: inventory-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Verification

The verification objective for inventory-service 2.9.1 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats INV-409 as the primary worked example while cross-checking INV-409, INV-503, KAFKA-302. Operators correlate gateway request IDs with inventory-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For INV-409, the catalog definition is: inventory-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Prevention

The prevention objective for inventory-service 2.9.1 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats INV-409 as the primary worked example while cross-checking INV-409, INV-503, KAFKA-302. Operators correlate gateway request IDs with inventory-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For INV-409, the catalog definition is: inventory-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.