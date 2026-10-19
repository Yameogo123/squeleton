from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from {{ cookiecutter.package_slug }}.core.config import settings
from {{ cookiecutter.package_slug }}.data.database import ping
from {{ cookiecutter.package_slug }}.utils.limiter import limiter

r_health = APIRouter()


@r_health.get("/health")
@limiter.exempt
async def health(request: Request):
    """Liveness: the process answers."""
    return {"status": "ok", "version": settings.APP_VERSION}


@r_health.get("/ready")
@limiter.exempt
async def ready(request: Request):
    """Readiness: dependencies are reachable (use it for load balancer / k8s probes)."""
    db_ok = await ping()
    return JSONResponse({"status": "ok" if db_ok else "degraded", "database": db_ok}, status_code=200 if db_ok else 503)
