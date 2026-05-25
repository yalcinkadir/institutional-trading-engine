# Quarterly Secrets Rotation Policy

This project uses GitHub Actions secrets for external service access. Secrets must be treated as production-sensitive credentials even when the system is used only for research and decision support.

## Scope

Current known secret:

```text
POLYGON_API_KEY
```

This policy also applies to any future secrets, including but not limited to:

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
REPORT_WEBHOOK_URL
BROKER_PAPER_API_KEY
BROKER_PAPER_API_SECRET
DATABASE_URL
```

## Rotation cadence

Secrets must be reviewed and rotated at least once per quarter.

Recommended schedule:

```text
January
April
July
October
```

Rotation should also happen immediately after:

```text
suspected leak
accidental log exposure
repository visibility change
team member access change
provider-side compromise
unexpected API usage spike
failed security review
```

## Rotation procedure

1. Create a new credential in the provider portal.
2. Add or update the GitHub Actions secret under:

```text
Settings → Secrets and variables → Actions
```

3. Run the smallest safe smoke test that proves the new secret works.
4. Revoke the old credential in the provider portal.
5. Check GitHub Actions logs for accidental credential exposure.
6. Record the rotation in the operations log or issue tracker.

## Validation commands

Polygon smoke test:

```bash
POLYGON_API_KEY=... python scripts/build_polygon_universe.py --max-symbols 25
```

Phase A regression after secret changes:

```bash
pytest tests/test_polygon_data_pipeline.py -q
pytest tests/test_polygon_structured_logging.py -q
pytest -q
```

## Logging rule

Never print secrets directly or indirectly. Logs may include:

```text
secret_name
provider
rotation_date
validation_status
```

Logs must not include:

```text
secret value
full authorization header
API key query parameter
provider dashboard screenshots containing credentials
```

## Fail-closed rule

If a required secret is missing or invalid, workflows should fail closed. The system must not silently switch to fabricated data or incomplete evidence.

## Phase B gate

Before Phase B starts, confirm:

```text
POLYGON_API_KEY exists in GitHub Actions secrets
last rotation date is known
rotation owner is known
no secret values appear in repository files
no secret values appear in recent workflow logs
```

## Ownership

The project owner is responsible for quarterly review until a formal operations role exists.
