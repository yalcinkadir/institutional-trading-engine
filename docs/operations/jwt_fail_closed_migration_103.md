# JWT Fail-Closed Migration Closure — Issue #103

Status date: 2026-06-11
Status: Closed / verified by existing implementation and guard tests
Scope: API authentication safety boundary

## Purpose

Issue #103 exists to ensure that JWT authentication never falls back to an insecure implicit default secret and never authorizes protected API access when authentication configuration is missing, blank or invalid.

This closure note records the verified fail-closed behavior and links it to the current code and test coverage.

## Safety invariant

```text
Protected API routes must fail closed when JWT authentication is not explicitly configured.

A missing or blank INSTITUTIONAL_JWT_SECRET must not create tokens, validate tokens, or silently fall back to a default development secret.
```

## Verified implementation

The JWT implementation uses the environment variable:

```text
INSTITUTIONAL_JWT_SECRET
```

The implementation refuses to operate when this variable is missing or blank:

```text
src/api/jwt_auth.py
- _get_jwt_secret() reads INSTITUTIONAL_JWT_SECRET.
- Missing or blank values raise JWTSecretNotConfiguredError.
- create_access_token() calls _get_jwt_secret() before token creation.
- validate_access_token() calls _get_jwt_secret() before token decoding.
```

Protected API dependencies convert this configuration failure into a visible service-unavailable response instead of accepting the request:

```text
src/api/security.py
- require_permission() validates bearer tokens through validate_access_token().
- JWTSecretNotConfiguredError is converted to HTTP 503.
- Missing authorization headers, malformed bearer headers and empty bearer tokens return HTTP 401.
- Role authorization remains enforced through validate_permission().
```

## Guard tests

The dangerous paths are covered by dedicated tests:

```text
tests/test_jwt_auth.py
- test_jwt_auth_fails_closed_without_configured_secret
- test_jwt_auth_fails_closed_with_blank_configured_secret
- test_validate_access_token_rejects_token_signed_with_wrong_secret
- test_validate_access_token_rejects_expired_token
- test_validate_access_token_rejects_invalid_role

tests/test_security_layer.py
- test_metrics_requires_jwt_token
- test_metrics_accepts_admin_token
- test_viewer_cannot_access_metrics
- test_metrics_rejects_malformed_authorization_header
- test_metrics_rejects_empty_bearer_token
- test_metrics_fails_closed_when_jwt_secret_is_not_configured
```

## Acceptance criteria mapping

| Requirement | Status | Evidence |
|---|---|---|
| No implicit/default JWT secret | Verified | `src/api/jwt_auth.py::_get_jwt_secret` |
| Missing secret blocks token creation | Verified | `test_jwt_auth_fails_closed_without_configured_secret` |
| Missing secret blocks token validation | Verified | `test_jwt_auth_fails_closed_without_configured_secret` |
| Blank secret blocks token creation and validation | Verified | `test_jwt_auth_fails_closed_with_blank_configured_secret` |
| Protected route fails closed when JWT config is missing | Verified | `test_metrics_fails_closed_when_jwt_secret_is_not_configured` |
| Forged/wrong-secret JWT is rejected | Verified | `test_validate_access_token_rejects_token_signed_with_wrong_secret` |
| Expired JWT is rejected | Verified | `test_validate_access_token_rejects_expired_token` |
| Invalid role is rejected | Verified | `test_validate_access_token_rejects_invalid_role` |
| Viewer cannot access admin metrics route | Verified | `test_viewer_cannot_access_metrics` |

## Validation command

Targeted validation command:

```bash
pytest -q tests/test_jwt_auth.py tests/test_security_layer.py
```

Full regression command:

```bash
pytest -q
```

## Closure decision

Issue #103 can be closed as verified because the code already implements the required fail-closed behavior and the dangerous paths are explicitly guarded by tests.

No live trading, broker execution, capital allocation or production deployment is authorized by this closure.
