from src.api.jwt_auth import create_access_token, validate_access_token


def test_create_and_validate_token():
    token = create_access_token("institutional-user")

    payload = validate_access_token(token)

    assert payload["sub"] == "institutional-user"
