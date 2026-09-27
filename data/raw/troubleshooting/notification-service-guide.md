---
document_id: DOC-NOTIFICATION-007
title: Notification Service Operations and Troubleshooting Guide
document_type: troubleshooting
service: notification-service
version: 2.2
product: nexora-commerce
created_at: 2025-01-10
updated_at: 2026-03-20
environment: [staging, production]
tags: [notification-service, troubleshooting, NOTIFY-429]
severity: 
---

# Notification Service Operations and Troubleshooting Guide

## Scope

This guide is the current operating reference owned by Customer Messaging. It covers versions 2.1, 2.2 and dependencies Kafka.

## Triage

The triage objective for notification-service 2.2 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats NOTIFY-429 as the primary worked example while cross-checking NOTIFY-429, KAFKA-305. Operators correlate gateway request IDs with notification-service traces and review Kafka saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For NOTIFY-429, the catalog definition is: notification-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Diagnosis

The diagnosis objective for notification-service 2.2 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats NOTIFY-429 as the primary worked example while cross-checking NOTIFY-429, KAFKA-305. Operators correlate gateway request IDs with notification-service traces and review Kafka saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For NOTIFY-429, the catalog definition is: notification-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Containment

The containment objective for notification-service 2.2 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats NOTIFY-429 as the primary worked example while cross-checking NOTIFY-429, KAFKA-305. Operators correlate gateway request IDs with notification-service traces and review Kafka saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For NOTIFY-429, the catalog definition is: notification-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Recovery

The recovery objective for notification-service 2.2 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats NOTIFY-429 as the primary worked example while cross-checking NOTIFY-429, KAFKA-305. Operators correlate gateway request IDs with notification-service traces and review Kafka saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For NOTIFY-429, the catalog definition is: notification-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Verification

The verification objective for notification-service 2.2 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats NOTIFY-429 as the primary worked example while cross-checking NOTIFY-429, KAFKA-305. Operators correlate gateway request IDs with notification-service traces and review Kafka saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For NOTIFY-429, the catalog definition is: notification-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Prevention

The prevention objective for notification-service 2.2 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats NOTIFY-429 as the primary worked example while cross-checking NOTIFY-429, KAFKA-305. Operators correlate gateway request IDs with notification-service traces and review Kafka saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For NOTIFY-429, the catalog definition is: notification-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.