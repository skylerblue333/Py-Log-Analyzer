# Changelog

## 0.1.0 — Engineering beta

- establish one canonical FastAPI log-triage service
- add bounded structured log batches and strict level/message/source validation
- add deterministic severity and source summaries
- add liveness/readiness endpoints and real tests
- replace fake Node build/test scripts with enforced Python compile, Ruff, pytest and dependency-audit gates
- add non-root container packaging and runtime health smoke verification
- document SKYCOIN4444 integration and explicit security/product boundaries

No durable ingestion, SIEM, alerting, anomaly ML, HA, or production deployment is claimed.
