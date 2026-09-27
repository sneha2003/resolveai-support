---
document_id: DOC-SEARCH-009
title: Search Service Operations and Troubleshooting Guide
document_type: troubleshooting
service: search-service
version: 4.5
product: nexora-commerce
created_at: 2025-01-10
updated_at: 2026-03-20
environment: [staging, production]
tags: [search-service, troubleshooting, SEARCH-429]
severity: 
---

# Search Service Operations and Troubleshooting Guide

## Scope

This guide is the current operating reference owned by Discovery Platform. It covers versions 4.4, 4.5 and dependencies OpenSearch, Kafka.

## Triage

The triage objective for search-service 4.5 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats SEARCH-429 as the primary worked example while cross-checking SEARCH-429, SEARCH-503. Operators correlate gateway request IDs with search-service traces and review OpenSearch, Kafka saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For SEARCH-429, the catalog definition is: search-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Diagnosis

The diagnosis objective for search-service 4.5 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats SEARCH-429 as the primary worked example while cross-checking SEARCH-429, SEARCH-503. Operators correlate gateway request IDs with search-service traces and review OpenSearch, Kafka saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For SEARCH-429, the catalog definition is: search-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Containment

The containment objective for search-service 4.5 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats SEARCH-429 as the primary worked example while cross-checking SEARCH-429, SEARCH-503. Operators correlate gateway request IDs with search-service traces and review OpenSearch, Kafka saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For SEARCH-429, the catalog definition is: search-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Recovery

The recovery objective for search-service 4.5 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats SEARCH-429 as the primary worked example while cross-checking SEARCH-429, SEARCH-503. Operators correlate gateway request IDs with search-service traces and review OpenSearch, Kafka saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For SEARCH-429, the catalog definition is: search-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Verification

The verification objective for search-service 4.5 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats SEARCH-429 as the primary worked example while cross-checking SEARCH-429, SEARCH-503. Operators correlate gateway request IDs with search-service traces and review OpenSearch, Kafka saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For SEARCH-429, the catalog definition is: search-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Prevention

The prevention objective for search-service 4.5 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. The guide treats SEARCH-429 as the primary worked example while cross-checking SEARCH-429, SEARCH-503. Operators correlate gateway request IDs with search-service traces and review OpenSearch, Kafka saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For SEARCH-429, the catalog definition is: search-service rejected or could not complete an operation because a required dependency or invariant failed. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.