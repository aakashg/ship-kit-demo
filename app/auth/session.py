import time

# Toy session store: token -> expiry (unix seconds). A real service reads a signed token.
SESSIONS = {
    "tok_live": 4102444800,     # 2100-01-01
    "tok_expired": 1731900000,  # 2024-11-18
}


class SessionExpired(Exception):
    pass


class UnknownSession(Exception):
    pass


def validate_session(token, now=None):
    now = time.time() if now is None else now
    if token not in SESSIONS:
        raise UnknownSession(token)
    exp = SESSIONS[token]
    if exp < now:
        raise SessionExpired(f"token exp={exp} < now")
    return {"token": token, "exp": exp}


def require_session(token, now=None):
    """validate_session for a request handler: unknown or expired sessions become a 401, never a 500."""
    from fastapi import HTTPException

    try:
        return validate_session(token, now)
    except UnknownSession:
        raise HTTPException(status_code=401, detail="unknown session")
    except SessionExpired:
        raise HTTPException(status_code=401, detail="session expired")
