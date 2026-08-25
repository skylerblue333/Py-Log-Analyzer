# Security Policy

## Supported status

Sky Log Triage is an **engineering beta**. CI verifies compilation, linting, tests, dependency audit, container build, non-root execution, and a liveness smoke check. These checks do not establish production security or deployment readiness.

## Current boundaries

The service bounds request size by entry count and field lengths and validates log levels. It does not redact secrets or personal data from submitted messages, authenticate callers, authorize tenants, rate-limit clients, persist logs, encrypt stored data, or provide durable audit retention.

Treat log payloads as potentially sensitive. Do not submit credentials, access tokens, private keys, or regulated/customer data unless a separate reviewed redaction and transport layer is in place.

## Reporting

Report suspected vulnerabilities privately through GitHub security reporting when available. Do not paste sensitive production logs into public issues.
