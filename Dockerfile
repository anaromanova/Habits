FROM python:3.10-slim

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY pyproject.toml poetry.lock ./
RUN pip install poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-root --without dev

COPY . .
