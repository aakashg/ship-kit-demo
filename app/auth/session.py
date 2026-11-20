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
