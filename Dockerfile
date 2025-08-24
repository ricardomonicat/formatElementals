# syntax=docker/dockerfile:1.7
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python -m pip install --upgrade pip && \
    pip install -r requirements-dev.txt && \
    pip install -e packages/actionformats[dev] && \
    pip install -e packages/elementals[dev]

CMD ["pytest", "-q"]
