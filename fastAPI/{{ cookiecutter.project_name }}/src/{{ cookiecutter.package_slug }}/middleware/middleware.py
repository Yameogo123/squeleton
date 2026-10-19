"""JWT authentication: token creation + `JWTBearer` dependency returning the token payload."""

from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from {{ cookiecutter.package_slug }}.core.config import settings

_UNAUTHORIZED = {"WWW-Authenticate": "Bearer"}


def token_response(access_token: str) -> dict:
    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    return {"access_token": access_token, "token_type": "Bearer", "expires_in": expires_in}


def signJWT(user_id: str, role: str = "user") -> dict:
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token_response(token)


def decodeJWT(token: str) -> dict | None:
    try:
        # pyjwt checks `exp` itself; `algorithms` is pinned to avoid alg-confusion attacks
        return jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"require": ["exp", "sub"]}
        )
    except jwt.PyJWTError:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=False)
        self._raise = auto_error

    async def __call__(self, request: Request) -> dict | None:
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        payload = decodeJWT(credentials.credentials) if credentials and credentials.scheme.lower() == "bearer" else None
        if payload is None:
            if self._raise:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token", headers=_UNAUTHORIZED)
            return None
        request.state.user = payload
        return payload


get_current_user = JWTBearer()


def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user.get("role") != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin only")
    return user


def ensure_owner_or_admin(user: dict, resource_user_id: str) -> None:
    """Prevents IDOR: a user may only act on its own resources unless admin."""
    if user.get("sub") != str(resource_user_id) and user.get("role") != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")
