from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi.middleware import SlowAPIMiddleware

from {{ cookiecutter.package_slug }}.core.config import settings
from {{ cookiecutter.package_slug }}.core.errors import register_exception_handlers
from {{ cookiecutter.package_slug }}.core.logging import setup_logging
from {{ cookiecutter.package_slug }}.middleware.http import BodySizeLimitMiddleware, RequestContextMiddleware, SecurityHeadersMiddleware
from {{ cookiecutter.package_slug }}.router.r_file import r_file
from {{ cookiecutter.package_slug }}.router.r_health import r_health
from {{ cookiecutter.package_slug }}.router.r_user import r_user
from {{ cookiecutter.package_slug }}.utils.limiter import limiter
from {{ cookiecutter.package_slug }}.utils.scheduling import lifespan

setup_logging()

# API docs are disabled in production (they expose the whole attack surface)
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    summary="{{ cookiecutter.description }}",
    lifespan=lifespan,
    docs_url=None if settings.is_prod else "/docs",
    redoc_url=None if settings.is_prod else "/redoc",
    openapi_url=None if settings.is_prod else "/openapi.json",
)
app.state.limiter = limiter
register_exception_handlers(app)

# Middlewares: the LAST added is the OUTERMOST (runs first on the request).
app.add_middleware(SlowAPIMiddleware)  # applies RATE_LIMIT_DEFAULT to every route
app.add_middleware(GZipMiddleware, minimum_size=1024)
app.add_middleware(BodySizeLimitMiddleware, max_size=settings.MAX_BODY_SIZE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    # browsers reject credentials with a wildcard origin
    allow_credentials="*" not in settings.ALLOW_ORIGINS,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
    max_age=600,
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
app.add_middleware(SecurityHeadersMiddleware, hsts=settings.is_prod)
app.add_middleware(RequestContextMiddleware)

BASE_DIR = Path(__file__).resolve().parent
static_dir = BASE_DIR / "html"
app.mount("/webui", StaticFiles(directory=static_dir), name="webui")
templates = Jinja2Templates(directory=static_dir)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_root(request: Request):
    return templates.TemplateResponse(request, "welcome.html", {"name": settings.APP_NAME})


app.include_router(r_health, tags=["health"])
app.include_router(r_user, prefix="/user", tags=["user"])
app.include_router(r_file, prefix="", tags=["file"])
