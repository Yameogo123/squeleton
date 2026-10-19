"""HTTP middlewares, written as pure ASGI (no BaseHTTPMiddleware) so streaming responses and
background tasks keep working and the overhead stays minimal.

- RequestContextMiddleware: request id (X-Request-ID), duration (X-Process-Time), access log
- SecurityHeadersMiddleware: OWASP recommended response headers
- BodySizeLimitMiddleware: rejects oversized request bodies with 413
"""

import re
import time
import uuid

from loguru import logger
from starlette.datastructures import MutableHeaders
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

_VALID_REQUEST_ID = re.compile(r"^[A-Za-z0-9\-_.]{1,64}$")
_QUIET_PATHS = {"/health", "/ready"}


class RequestContextMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        incoming = dict(scope["headers"]).get(b"x-request-id", b"").decode("latin-1")
        # never trust a client value blindly: it ends up in logs
        request_id = incoming if _VALID_REQUEST_ID.match(incoming) else uuid.uuid4().hex
        scope.setdefault("state", {})["request_id"] = request_id
        start = time.perf_counter()
        status_code = 500

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
                headers = MutableHeaders(scope=message)
                headers["X-Request-ID"] = request_id
                headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}"
            await send(message)

        with logger.contextualize(request_id=request_id):
            try:
                await self.app(scope, receive, send_wrapper)
            finally:
                if scope["path"] not in _QUIET_PATHS:
                    duration_ms = (time.perf_counter() - start) * 1000
                    client = scope.get("client") or ("-", 0)
                    logger.info(f'{client[0]} "{scope["method"]} {scope["path"]}" {status_code} {duration_ms:.1f}ms')


class SecurityHeadersMiddleware:
    def __init__(self, app: ASGIApp, hsts: bool = False) -> None:
        self.app = app
        self.hsts = hsts

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.setdefault("X-Content-Type-Options", "nosniff")
                headers.setdefault("X-Frame-Options", "DENY")
                headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
                headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
                headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
                # strict CSP for API payloads only: /docs and the welcome page load CDN assets
                if headers.get("content-type", "").startswith("application/json"):
                    headers.setdefault("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
                if self.hsts:
                    headers.setdefault("Strict-Transport-Security", "max-age=63072000; includeSubDomains")
            await send(message)

        await self.app(scope, receive, send_wrapper)


class _BodyTooLarge(HTTPException):
    # an HTTPException so FastAPI's body parsing re-raises it untouched -> handled as a 413
    def __init__(self) -> None:
        super().__init__(status_code=413, detail="Request body too large")


class BodySizeLimitMiddleware:
    def __init__(self, app: ASGIApp, max_size: int) -> None:
        self.app = app
        self.max_size = max_size

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        too_large = JSONResponse({"detail": "Request body too large"}, status_code=413)
        content_length = dict(scope["headers"]).get(b"content-length")
        if content_length and content_length.isdigit() and int(content_length) > self.max_size:
            return await too_large(scope, receive, send)

        # chunked uploads have no content-length: count bytes while they are read
        received = 0
        response_started = False

        async def receive_wrapper() -> Message:
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > self.max_size:
                    raise _BodyTooLarge
            return message

        async def send_wrapper(message: Message) -> None:
            nonlocal response_started
            if message["type"] == "http.response.start":
                response_started = True
            await send(message)

        try:
            await self.app(scope, receive_wrapper, send_wrapper)
        except _BodyTooLarge:
            if not response_started:
                await too_large(scope, receive, send)
