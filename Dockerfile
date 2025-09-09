# Multi-arch, slim Python base
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000 \
    UVICORN_WORKERS=1

WORKDIR /app

# System deps (optional but handy for wheels)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY manus2 ./manus2

# Health check (Railway/other PaaS ignore, but good practice)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD curl -fsS http://localhost:${PORT}/health || exit 1

EXPOSE ${PORT}
CMD ["uvicorn", "manus2.app:api", "--host", "0.0.0.0", "--port", "8000"]
