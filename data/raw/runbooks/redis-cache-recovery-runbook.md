---
document_id: RUN-REDIS-001
title: Redis Cache Recovery Runbook
document_type: runbook
service: authentication-service
version: 5.1.2
product: nexora-commerce
created_at: 2025-01-10
updated_at: 2026-03-20
environment: [staging, production]
tags: [runbook, authentication-service, CACHE-118]
severity: 
---

# Redis Cache Recovery Runbook

## Purpose and prerequisites

This runbook provides a controlled production procedure. The incident commander, service owner, and communications lead must be identified before mutations begin. Confirm dashboard access, an approved change record, the last known-good revision, and a rollback checkpoint.

## Triage

The triage objective for authentication-service 5.1.2 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. Every command requires a named operator and a peer verifier. Do not improvise database or payment changes from memory. Operators correlate gateway request IDs with authentication-service traces and review Redis, PostgreSQL 16 saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For CACHE-118, the catalog definition is: authentication-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Diagnosis

The diagnosis objective for authentication-service 5.1.2 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. Every command requires a named operator and a peer verifier. Do not improvise database or payment changes from memory. Operators correlate gateway request IDs with authentication-service traces and review Redis, PostgreSQL 16 saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For CACHE-118, the catalog definition is: authentication-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Containment

The containment objective for authentication-service 5.1.2 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. Every command requires a named operator and a peer verifier. Do not improvise database or payment changes from memory. Operators correlate gateway request IDs with authentication-service traces and review Redis, PostgreSQL 16 saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For CACHE-118, the catalog definition is: authentication-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Recovery

The recovery objective for authentication-service 5.1.2 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. Every command requires a named operator and a peer verifier. Do not improvise database or payment changes from memory. Operators correlate gateway request IDs with authentication-service traces and review Redis, PostgreSQL 16 saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For CACHE-118, the catalog definition is: authentication-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Verification

The verification objective for authentication-service 5.1.2 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. Every command requires a named operator and a peer verifier. Do not improvise database or payment changes from memory. Operators correlate gateway request IDs with authentication-service traces and review Redis, PostgreSQL 16 saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For CACHE-118, the catalog definition is: authentication-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Prevention

The prevention objective for authentication-service 5.1.2 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. Every command requires a named operator and a peer verifier. Do not improvise database or payment changes from memory. Operators correlate gateway request IDs with authentication-service traces and review Redis, PostgreSQL 16 saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For CACHE-118, the catalog definition is: authentication-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.