---
document_id: DOC-ERR-001
title: Nexora Error Code Catalog
document_type: product_doc
service: platform
version: 
product: nexora-commerce
created_at: 2025-01-10
updated_at: 2026-03-20
environment: [staging, production]
tags: [errors, reference]
severity: 
---

# Nexora Error Code Catalog

## PAY-201: payment-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** payment-service  
**Severity:** SEV-3

### Symptoms and causes

payment-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## PAY-307: Payment authorization result remained indeterminate after the upstream processor deadline.

**Service:** payment-service  
**Severity:** SEV-3

### Symptoms and causes

Payment authorization result remained indeterminate after the upstream processor deadline. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Query the provider by idempotency key; never blindly repeat authorization. Fixed retry classification ships in 4.3.

## DB-104: Database connection acquisition timed out before a checkout transaction could begin.

**Service:** payment-service  
**Severity:** SEV-2

### Symptoms and causes

Database connection acquisition timed out before a checkout transaction could begin. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

For Payment Service 4.2 on PostgreSQL 16 set checkout pool maximumSize to 24, minimumIdle to 6, connectionTimeoutMs to 3000, then deploy 4.2.1, which restores version-aware pool sizing.

## DB-207: payment-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** payment-service  
**Severity:** SEV-3

### Symptoms and causes

payment-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## ORD-502: order-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** order-service  
**Severity:** SEV-2

### Symptoms and causes

order-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## ORD-504: order-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** order-service  
**Severity:** SEV-3

### Symptoms and causes

order-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## KAFKA-301: order-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** order-service  
**Severity:** SEV-3

### Symptoms and causes

order-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## AUTH-401: authentication-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** authentication-service  
**Severity:** SEV-2

### Symptoms and causes

authentication-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## AUTH-429: authentication-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** authentication-service  
**Severity:** SEV-3

### Symptoms and causes

authentication-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## CACHE-118: authentication-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** authentication-service  
**Severity:** SEV-3

### Symptoms and causes

authentication-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## INV-409: inventory-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** inventory-service  
**Severity:** SEV-3

### Symptoms and causes

inventory-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## INV-503: inventory-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** inventory-service  
**Severity:** SEV-2

### Symptoms and causes

inventory-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## KAFKA-302: inventory-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** inventory-service  
**Severity:** SEV-3

### Symptoms and causes

inventory-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## CAT-404: catalog-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** catalog-service  
**Severity:** SEV-3

### Symptoms and causes

catalog-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## SEARCH-206: catalog-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** catalog-service  
**Severity:** SEV-3

### Symptoms and causes

catalog-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## CART-409: cart-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** cart-service  
**Severity:** SEV-3

### Symptoms and causes

cart-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## CACHE-119: cart-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** cart-service  
**Severity:** SEV-3

### Symptoms and causes

cart-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## NOTIFY-429: notification-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** notification-service  
**Severity:** SEV-3

### Symptoms and causes

notification-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## KAFKA-305: notification-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** notification-service  
**Severity:** SEV-3

### Symptoms and causes

notification-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## GW-429: api-gateway rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** api-gateway  
**Severity:** SEV-3

### Symptoms and causes

api-gateway rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## GW-502: api-gateway rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** api-gateway  
**Severity:** SEV-3

### Symptoms and causes

api-gateway rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## SEARCH-429: search-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** search-service  
**Severity:** SEV-3

### Symptoms and causes

search-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## SEARCH-503: search-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** search-service  
**Severity:** SEV-3

### Symptoms and causes

search-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## CUS-409: customer-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** customer-service  
**Severity:** SEV-3

### Symptoms and causes

customer-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

## DB-211: customer-service rejected or could not complete an operation because a required dependency or invariant failed.

**Service:** customer-service  
**Severity:** SEV-3

### Symptoms and causes

customer-service rejected or could not complete an operation because a required dependency or invariant failed. The code is emitted with a request ID and dependency state so operators can distinguish transient saturation from a persistent configuration mismatch.

### Diagnostic steps

1. Correlate the request id across gateway and service logs.
2. Compare active configuration with the version baseline.
3. Inspect dependency saturation and retry rates.

### Remediation

Stabilize the dependency, restore the documented configuration baseline, and verify with a canary request before clearing the alert.

