import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.llm import MaxTokensExceeded, complete

log = logging.getLogger("gateway")
app = FastAPI(title="toy-ai-gateway")


@app.get("/v1/me")
def me(token: str):
    from app.auth.session import validate_session
    claims = validate_session(token)
    return {"exp": claims["exp"]}


class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 256


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/v1/chat")
def chat(req: ChatRequest):
    try:
        result = complete(req.prompt, max_tokens=req.max_tokens)
    except MaxTokensExceeded as e:
        # Caller's prompt/max_tokens combination is the problem: 4xx, not 5xx.
        raise HTTPException(status_code=400, detail=str(e))
    return {"text": result["text"], "usage": result["completion_tokens"]}
