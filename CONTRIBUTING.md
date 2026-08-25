# Contributing to Sky Log Triage

## Development setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pip-audit
```

## Verification

Run the same core checks enforced by CI before opening a pull request:

```bash
python -m compileall -q src tests
ruff check src tests
pytest -q
pip-audit -r requirements.txt
```

For container changes also run:

```bash
docker build -t sky-log-triage .
docker run --rm --entrypoint=id sky-log-triage -u
```

The image must run as a non-root UID.

## Scope and style

- Keep the service focused on bounded structured log triage.
- Add tests for behavior changes and validation edge cases.
- Do not add claims of SIEM, durable ingestion, alerting, anomaly ML, or production deployment without corresponding implementation and evidence.
- Use clear commit messages and keep documentation aligned with supported behavior.

## Pull requests

1. Create a focused feature branch.
2. Make the smallest coherent change.
3. Run the verification commands above.
4. Document any security or compatibility boundary changes.
5. Open a pull request with a truthful status description.

## License

See `LICENSE`.
