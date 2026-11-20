from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_me_live_session():
    assert client.get("/v1/me", params={"token": "tok_live"}).status_code == 200
