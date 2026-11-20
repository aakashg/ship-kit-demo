import logging
from fastapi import FastAPI
from pydantic import BaseModel

from app.llm import complete

log = logging.getLogger("gateway")
app = FastAPI(title="toy-ai-gateway")


@app.get("/v1/me")
def me(token: str):
    from app.auth.session import require_session
    claims = require_session(token)
    return {"exp": claims["exp"]}


class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 256


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/v1/chat")
def chat(req: ChatRequest):
    result = complete(req.prompt, max_tokens=req.max_tokens)
    return {"text": result["text"], "usage": result["completion_tokens"]}
