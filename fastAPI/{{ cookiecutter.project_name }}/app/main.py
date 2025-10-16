from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from bson.objectid import ObjectId
from loguru import logger

from pathlib import Path

from {{ cookiecutter.package_slug }}.middleware.middleware import signJWT, JWTBearer
from {{ cookiecutter.package_slug }}.router.r_file import r_file
from {{ cookiecutter.package_slug }}.router.r_user import r_user
from {{ cookiecutter.package_slug }}.utils.scheduling import scheduler, add_jobs

from decouple import config

import pretty_errors  # noqa: F401

PORT = config("PORT")

# Create FastAPI app
app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
static_dir = BASE_DIR / "html"

app.mount("/webui", StaticFiles(directory=static_dir), name="webui")
templates = Jinja2Templates(directory=static_dir)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request, "name": "Backend"})




########### user
app.include_router(r_user, prefix="/user", tags=["user"])


########## file
app.include_router(r_file, prefix="", tags= ["file"])


######### scheduling

@app.on_event("startup")
async def startup_event():
    if not scheduler.running:
        add_jobs()
        scheduler.start()
        print("✅ Scheduler started in main process")

@app.on_event("shutdown")
async def shutdown_event():
    try:
        scheduler.shutdown()
    except Exception:
        print("scheduler already killed")

