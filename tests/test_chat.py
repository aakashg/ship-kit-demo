from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_healthz():
    assert client.get("/healthz").status_code == 200


def test_chat_ok():
    r = client.post("/v1/chat", json={"prompt": "hello", "max_tokens": 64})
    assert r.status_code == 200


def test_chat_prompt_longer_than_max_tokens_is_client_error():
    # prompt ~200 tokens, caller allows only 128: client-caused, must be 4xx not 500
    r = client.post("/v1/chat", json={"prompt": "x" * 800, "max_tokens": 128})
    assert r.status_code == 400
    assert "max_tokens" in r.json()["detail"]
