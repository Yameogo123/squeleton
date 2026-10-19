from slowapi import Limiter
from slowapi.util import get_remote_address

from {{ cookiecutter.package_slug }}.core.config import settings

# Redis storage shares the counters between workers/replicas; memory is per process.
# Behind a reverse proxy, run uvicorn with --proxy-headers so the client IP is the real one.
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.RATE_LIMIT_DEFAULT],
    storage_uri=settings.REDIS_URL or "memory://",
    headers_enabled=False,
)
