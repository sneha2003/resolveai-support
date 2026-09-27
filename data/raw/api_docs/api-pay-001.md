---
document_id: API-PAY-001
title: Payment API
document_type: api_doc
service: payment-service
version: 4.3
product: nexora-commerce
created_at: 2025-01-10
updated_at: 2026-03-20
environment: [staging, production]
tags: [api, payment-service, PAY-307]
severity: 
---

# Payment API

## POST /api/v1/payments/authorize

Requires a bearer token and an `Idempotency-Key` for state-changing operations. Tenant and request identifiers are propagated to every downstream call. Rate-limit responses include a bounded `Retry-After`; clients must use exponential backoff with jitter.

```json
{"tenantId":"tenant-demo","amount":12500,"currency":"EUR","reference":"order-4815"}
```

A successful response contains the resource ID, state, version, and correlation ID. Error responses use `{"code":"PAY-307","message":"safe summary","requestId":"req-7f21"}`. Never use the human-readable message for program logic.

## Version behavior

Current clients must preserve idempotency keys across uncertain outcomes. Version negotiation uses the URL major version and additive response fields. Breaking schema changes require a new major endpoint.

## Triage

The triage objective for payment-service 4.3 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. API troubleshooting begins with the request ID, authentication state, rate-limit headers, and idempotency key. Operators correlate gateway request IDs with payment-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For PAY-307, the catalog definition is: Payment authorization result remained indeterminate after the upstream processor deadline. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Query the provider by idempotency key; never blindly repeat authorization. Fixed retry classification ships in 4.3. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Diagnosis

The diagnosis objective for payment-service 4.3 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. API troubleshooting begins with the request ID, authentication state, rate-limit headers, and idempotency key. Operators correlate gateway request IDs with payment-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For PAY-307, the catalog definition is: Payment authorization result remained indeterminate after the upstream processor deadline. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Query the provider by idempotency key; never blindly repeat authorization. Fixed retry classification ships in 4.3. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Containment

The containment objective for payment-service 4.3 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. API troubleshooting begins with the request ID, authentication state, rate-limit headers, and idempotency key. Operators correlate gateway request IDs with payment-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For PAY-307, the catalog definition is: Payment authorization result remained indeterminate after the upstream processor deadline. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Query the provider by idempotency key; never blindly repeat authorization. Fixed retry classification ships in 4.3. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Recovery

The recovery objective for payment-service 4.3 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. API troubleshooting begins with the request ID, authentication state, rate-limit headers, and idempotency key. Operators correlate gateway request IDs with payment-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For PAY-307, the catalog definition is: Payment authorization result remained indeterminate after the upstream processor deadline. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Query the provider by idempotency key; never blindly repeat authorization. Fixed retry classification ships in 4.3. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Verification

The verification objective for payment-service 4.3 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. API troubleshooting begins with the request ID, authentication state, rate-limit headers, and idempotency key. Operators correlate gateway request IDs with payment-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For PAY-307, the catalog definition is: Payment authorization result remained indeterminate after the upstream processor deadline. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Query the provider by idempotency key; never blindly repeat authorization. Fixed retry classification ships in 4.3. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.

## Prevention

The prevention objective for payment-service 4.3 is to preserve customer safety while collecting enough evidence to distinguish application health from dependency health. API troubleshooting begins with the request ID, authentication state, rate-limit headers, and idempotency key. Operators correlate gateway request IDs with payment-service traces and review PostgreSQL 16, Kafka, Redis saturation. A green Kubernetes readiness probe proves only that the process accepts traffic; it does not prove that downstream capacity is available.

For PAY-307, the catalog definition is: Payment authorization result remained indeterminate after the upstream processor deadline. The team checks service error rate, p95 latency, active and waiting connections, Kafka lag where applicable, and the deployment timeline. Evidence is recorded before changing configuration. Commands are executed through approved observability and deployment tooling; secrets and customer payloads must never be pasted into tickets.

Decision criteria are explicit. If the error began within thirty minutes of a version or configuration rollout, compare the live manifest with the release baseline. If dependency saturation is shared by several services, escalate to the platform owner. If only one tenant is affected, examine tenant routing and rate limits. The documented remediation is: Query the provider by idempotency key; never blindly repeat authorization. Fixed retry classification ships in 4.3. A canary must complete ten representative operations before broad restoration.

Rollback remains available until verification passes. Restore the previous immutable deployment revision, keep database migrations that are backward compatible, and stop if a downgrade would read data written in a newer incompatible format. Close the phase only after dashboards remain within the service-level objective for fifteen minutes and a synthetic checkout traverses API Gateway, Authentication, Cart, Inventory, Payment, Order, and Notification.