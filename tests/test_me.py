from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_me_live_session():
    assert client.get("/v1/me", params={"token": "tok_live"}).status_code == 200


def test_me_expired_session_is_401():
    r = client.get("/v1/me", params={"token": "tok_expired"})
    assert r.status_code == 401
    assert r.json()["detail"] == "session expired"


def test_me_unknown_session_is_401():
    assert client.get("/v1/me", params={"token": "nope"}).status_code == 401
