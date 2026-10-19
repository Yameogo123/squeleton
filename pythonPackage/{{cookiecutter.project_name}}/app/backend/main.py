from decouple import Csv, config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

PORT = config("PORT", default=8000, cast=int)
ALLOW_ORIGINS = config("ALLOW_ORIGINS", default="http://localhost:8501", cast=Csv())
ENVIRONMENT = config("ENVIRONMENT", default="dev")

# API docs only outside production
app = FastAPI(docs_url=None if ENVIRONMENT == "prod" else "/docs", redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials="*" not in ALLOW_ORIGINS,  # browsers reject credentials with a wildcard
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI with Uvicorn!"}


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=ENVIRONMENT == "dev")  # noqa: S104
