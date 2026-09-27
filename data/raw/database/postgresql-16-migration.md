---
document_id: DB-MIG-016
title: PostgreSQL 16 Migration and Pool Sizing Guide
document_type: database
service: payment-service
version: 4.2.1
product: nexora-commerce
created_at: 2025-01-10
updated_at: 2026-03-20
environment: [staging, production]
tags: [postgresql, migration, DB-104]
severity: 
---

# PostgreSQL 16 Migration and Pool Sizing Guide

## Capacity formula

Reserve 20 percent of PostgreSQL sessions for administration and migrations. Divide the remaining service budget by the maximum production replica count, not the current count. For Payment Service 4.2.1 the approved baseline is maximumSize 24, minimumIdle 6, connectionTimeoutMs 3000. Payment Service 4.2 used 40 per pod and can trigger DB-104 with twelve replicas against a 300-session budget.

## Triage

The triage objective for payment-service 4.2.1 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. Migration rehearsals must use PostgreSQL 16 and production-equivalent replica counts. Operators correlate gateway request IDs with payment-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For DB-104, the catalog definition is: Database connection acquisition timed out before a checkout transaction could begin. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: For Payment Service 4.2 on PostgreSQL 16 set checkout pool maximumSize to 24, minimumIdle to 6, connectionTimeoutMs to 3000, then deploy 4.2.1, which restores version-aware pool sizing. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Diagnosis

The diagnosis objective for payment-service 4.2.1 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. Migration rehearsals must use PostgreSQL 16 and production-equivalent replica counts. Operators correlate gateway request IDs with payment-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For DB-104, the catalog definition is: Database connection acquisition timed out before a checkout transaction could begin. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: For Payment Service 4.2 on PostgreSQL 16 set checkout pool maximumSize to 24, minimumIdle to 6, connectionTimeoutMs to 3000, then deploy 4.2.1, which restores version-aware pool sizing. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Containment

The containment objective for payment-service 4.2.1 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. Migration rehearsals must use PostgreSQL 16 and production-equivalent replica counts. Operators correlate gateway request IDs with payment-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For DB-104, the catalog definition is: Database connection acquisition timed out before a checkout transaction could begin. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: For Payment Service 4.2 on PostgreSQL 16 set checkout pool maximumSize to 24, minimumIdle to 6, connectionTimeoutMs to 3000, then deploy 4.2.1, which restores version-aware pool sizing. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Recovery

The recovery objective for payment-service 4.2.1 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. Migration rehearsals must use PostgreSQL 16 and production-equivalent replica counts. Operators correlate gateway request IDs with payment-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For DB-104, the catalog definition is: Database connection acquisition timed out before a checkout transaction could begin. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: For Payment Service 4.2 on PostgreSQL 16 set checkout pool maximumSize to 24, minimumIdle to 6, connectionTimeoutMs to 3000, then deploy 4.2.1, which restores version-aware pool sizing. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Verification

The verification objective for payment-service 4.2.1 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. Migration rehearsals must use PostgreSQL 16 and production-equivalent replica counts. Operators correlate gateway request IDs with payment-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For DB-104, the catalog definition is: Database connection acquisition timed out before a checkout transaction could begin. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: For Payment Service 4.2 on PostgreSQL 16 set checkout pool maximumSize to 24, minimumIdle to 6, connectionTimeoutMs to 3000, then deploy 4.2.1, which restores version-aware pool sizing. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Prevention

The prevention objective for payment-service 4.2.1 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. Migration rehearsals must use PostgreSQL 16 and production-equivalent replica counts. Operators correlate gateway request IDs with payment-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For DB-104, the catalog definition is: Database connection acquisition timed out before a checkout transaction could begin. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: For Payment Service 4.2 on PostgreSQL 16 set checkout pool maximumSize to 24, minimumIdle to 6, connectionTimeoutMs to 3000, then deploy 4.2.1, which restores version-aware pool sizing. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.