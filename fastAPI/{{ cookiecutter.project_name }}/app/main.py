from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from slowapi.errors import RateLimitExceeded

from {{ cookiecutter.package_slug }}.router.r_file import r_file
from {{ cookiecutter.package_slug }}.router.r_user import r_user

from {{ cookiecutter.package_slug }}.utils.limiter import limiter
from {{ cookiecutter.package_slug }}.utils.scheduling import lifespan

from decouple import config

import pretty_errors  # noqa: F401

PORT = config("PORT")
ALLOW_ORIGIN = config("ALLOW_ORIGIN")

# Create FastAPI app
app = FastAPI(title="backend", version="0.0.1", lifespan=lifespan, summary='It is all my app backend', docs_url="/docs")
app.state.limiter = limiter

BASE_DIR = Path(__file__).resolve().parent
static_dir = BASE_DIR / "html"

app.mount("/webui", StaticFiles(directory=static_dir), name="webui")
templates = Jinja2Templates(directory=static_dir)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOW_ORIGIN], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request, "name": "Backend"})

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Beaucoup d'appels! Allez y doucement!"}
    )


########### user
app.include_router(r_user, prefix="/user", tags=["user"])


########## file
app.include_router(r_file, prefix="", tags= ["file"])



