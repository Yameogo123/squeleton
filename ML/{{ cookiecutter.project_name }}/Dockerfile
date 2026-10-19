FROM python:{{ cookiecutter.python_version }}-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 ENVIRONMENT=prod PORT=8000
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app

# deps first (cached layer), then the code
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt
COPY . .
RUN uv pip install --system --no-cache --no-deps . \
    && useradd --create-home --uid 10001 appuser && chown -R appuser /app
USER appuser

# Streamlit / FastAPI
EXPOSE 8501 8000

CMD ["sh", "-c", "cd app/backend && exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --proxy-headers --no-server-header"]
