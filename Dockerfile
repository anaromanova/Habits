FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root

COPY . .

RUN python manage.py migrate --noinput \
    && python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "habits_project.config.wsgi:application", "--workers=4", "--bind=0.0.0.0:8000"]