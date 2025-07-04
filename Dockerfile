FROM python:3.10-slim

WORKDIR /app

# 1) Системные зависимости (включая curl и netcat)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      curl \
      netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# 2) Обновляем pip и ставим Poetry официальным скриптом
RUN pip install --upgrade pip \
 && curl -sSL https://install.python-poetry.org | python3 -

# 3) Добавляем ~/.local/bin (где Poetry положил бинарь) в PATH
ENV PATH="/root/.local/bin:${PATH}"

# 4) Копируем только манифесты и ставим зависимости без dev
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --without dev

# 5) Копируем всё приложение и собираем статику
COPY . .
RUN poetry run python manage.py collectstatic --noinput

# 6) На старте контейнера дожидаемся базы, мигрируем и запускаем Gunicorn
ENV PORT=8000
EXPOSE ${PORT}

CMD ["sh", "-c", "\
  echo \"Waiting for DB $DATABASE_HOST:$DATABASE_PORT...\"; \
  until nc -z $DATABASE_HOST $DATABASE_PORT; do sleep 1; done; \
  echo \"DB is up, running migrations...\"; \
  poetry run python manage.py migrate --noinput; \
  echo \"Starting Gunicorn\"; \
  exec gunicorn habits_project.config.wsgi:application --bind 0.0.0.0:${PORT}\
"]
