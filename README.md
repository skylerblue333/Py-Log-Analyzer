# Sky Log Triage — Python Engineering Beta

Sky Log Triage is a focused FastAPI service for analyzing bounded batches of structured log entries and returning deterministic severity and source summaries.

## Status

**Engineering beta.** The service validates structured input, caps each request at 1,000 log entries, limits message/source sizes, provides liveness/readiness endpoints, has automated tests, dependency auditing, and non-root container verification.

It does **not** claim log collection agents, durable log storage, SIEM correlation, anomaly-detection ML, alert delivery, tenant isolation, HA, or production deployment.

## API

- `GET /healthz` — process liveness.
- `GET /readyz` — current request-capacity contract.
- `POST /v1/analyze` — analyze a JSON object with a `logs` array.

Supported levels are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`. `ERROR` and `CRITICAL` are counted as severe.

Example:

```bash
curl -s -X POST http://127.0.0.1:8000/v1/analyze \
  -H 'content-type: application/json' \
  -d '{"logs":[{"level":"INFO","message":"started","source":"api"},{"level":"ERROR","message":"failed","source":"worker"}]}'
```

## Run locally

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 127.0.0.1 --port 8000
```

## Verify

```bash
python -m compileall -q src tests
ruff check src tests
pytest -q
pip-audit -r requirements.txt
docker build -t sky-log-triage .
docker run --rm --entrypoint=id sky-log-triage -u
```

The container is expected to run as UID `10001`. CI also starts the image and verifies `/healthz`.

## Architecture

`src/main.py` is the canonical service. Validation is performed at the HTTP boundary through Pydantic models. Analysis is intentionally deterministic and in-memory: it summarizes the submitted batch and retains no logs after the request completes.

## SKYCOIN4444 integration

Use this component as a stateless triage boundary for batches already collected by ecosystem services. Do not send secrets or unrestricted raw production logs without a separate redaction and transport policy. Durable observability should remain in the platform's logging/telemetry infrastructure rather than being implied by this service.

## Security and operational boundaries

The service does not provide authentication, authorization, rate limiting, log redaction, encrypted storage, durable audit retention, or tenant isolation. Put appropriate gateway controls in front of it before use outside a trusted development environment.

## License

See `LICENSE`.
