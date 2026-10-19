from {{ cookiecutter.package_slug }}.entity.User import User
from {{ cookiecutter.package_slug }}.middleware.middleware import decodeJWT, signJWT
from {{ cookiecutter.package_slug }}.utils.controller import blind_index, decrypt_text, encrypt_text, hash_pwd, verify_password


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_security_headers_and_request_id(client):
    response = client.get("/health", headers={"X-Request-ID": "abc-123"})
    assert response.headers["X-Request-ID"] == "abc-123"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "X-Process-Time" in response.headers


def test_malicious_request_id_is_replaced(client):
    response = client.get("/health", headers={"X-Request-ID": "bad\nvalue"})
    assert response.headers["X-Request-ID"] != "bad\nvalue"


def test_protected_route_requires_token(client):
    assert client.get("/user/me").status_code == 401
    assert client.get("/user/me", headers={"Authorization": "Bearer nope"}).status_code == 401


def test_body_size_limit(client):
    from {{ cookiecutter.package_slug }}.core.config import settings

    body = b"x" * (settings.MAX_BODY_SIZE + 1)
    response = client.post("/user/login", content=body, headers={"Content-Type": "application/json"})
    assert response.status_code == 413


def test_validation_error_shape(client):
    response = client.post("/user/login", json={"email": "not-an-email", "password": "x"})
    assert response.status_code == 422
    assert "request_id" in response.json()


def test_jwt_roundtrip():
    token = signJWT("42", "admin")["access_token"]
    payload = decodeJWT(token)
    assert payload["sub"] == "42" and payload["role"] == "admin"
    assert decodeJWT(token + "x") is None


def test_crypto_helpers():
    assert decrypt_text(encrypt_text("Jean")) == "Jean"
    assert blind_index("A@b.com ") == blind_index("a@b.com")
    hashed = hash_pwd("Secret1!")
    assert verify_password("Secret1!", hashed)
    assert not verify_password("wrong", hashed)
    assert not verify_password("anything", None)


def test_public_user_hides_secrets():
    user = User.public({"_id": "1", "password": "h", "email_hash": "x", "nom": encrypt_text("Doe")})
    assert "password" not in user and "email_hash" not in user
    assert user["nom"] == "Doe"
