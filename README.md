# Habits

Сервис трекинга привычек с напоминаниями в Telegram.

---

## Содержание

* [Описание](#описание)
* [Требования](#требования)
* [Переменные окружения](#переменные-окружения)
* [Локальная установка (Poetry)](#локальная-установка-poetry)
* [Установка с Docker Compose](#установка-с-docker-compose)
* [Миграции и запуск](#миграции-и-запуск)
* [Проверка сервисов](#проверка-сервисов)
* [Остановка и очистка](#остановка-и-очистка)
* [Git и вклад](#git-и-вклад)

---

## Описание

Этот проект представляет сервис для отслеживания привычек с отправкой напоминаний пользователям через Telegram.

## Требования

* Python 3.10+
* Docker, Docker Compose (для запуска в контейнерах)
* Poetry (для локальной разработки)

## Переменные окружения

1. Скопируйте шаблон файла:

   ```bash
   cp .env.example .env
   ```
2. Откройте `.env` и заполните необходимые переменные:

   ```ini
   # PostgreSQL
   DATABASE_USER=your_user
   DATABASE_PASSWORD=your_password
   DATABASE_NAME=your_db
   DATABASE_HOST=host
   DATABASE_PORT=port

   # Django / FastAPI
   SECRET_KEY=your_secret_key
   DEBUG=True

   # Database URL
   DATABASE_URL=postgresql://${DATABASE_USER}:${DATABASE_PASSWORD}@db:5432/${DATABASE_NAME}
   # Telegram
   TELEGRAM_BOT_TOKEN=
   
   # Redis
   REDIS_URL=redis://redis:6379/0

   # Celery
   CELERY_BROKER_URL=${REDIS_URL}
   CELERY_RESULT_BACKEND=${REDIS_URL}

   # Telegram Bot
   TELEGRAM_TOKEN=your_telegram_bot_token
   ```
3. Файл `.env` добавлен в `.gitignore`, шаблон `.env.example` хранится в репозитории.

## Локальная установка (Poetry)

> Подходит для разработки без Docker.

```bash
git clone https://github.com/YourOrg/Habits.git
cd Habits_project
poetry install
cp .env.example .env
# Заполните .env
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Приложение будет доступно по адресу `http://localhost:8000/`.

## Установка с Docker Compose

> Быстрый старт с использованием контейнеров.

1. Склонируйте репозиторий и перейдите в корень проекта:

   ```bash
   git clone https://github.com/YourOrg/Habits.git
   cd Habits_project
   ```
2. Создайте файл `.env` на основе шаблона:

   ```bash
   cp .env.example .env
   # Отредактируйте .env
   ```
3. Запустите все сервисы:

   ```bash
   docker-compose up --build -d
   ```

Сервисы, описанные в `docker-compose.yml`:

* **db**: PostgreSQL на порту `5432`
* **redis**: Redis на порту `6379`
* **backend**: ваше приложение на порту `8000`
* **worker**: Celery worker
* **beat**: Celery Beat scheduler

## Миграции и запуск

При первом старте контейнера `backend` автоматически выполняется миграция:

```bash
# внутри контейнера backend
alembic upgrade head
```

Если нужно выполнить миграции вручную:

```bash
docker-compose exec backend alembic upgrade head
```

## Проверка сервисов

* **Backend**: `curl http://localhost:8000/health` (должен вернуть статус 200)
* **PostgreSQL**:

  ```bash
  docker-compose exec db psql -U $POSTGRES_USER -d $POSTGRES_DB
  ```
* **Redis**:

  ```bash
  docker-compose exec redis redis-cli ping
  ```
* **Celery Worker**:

  ```bash
  docker-compose logs -f worker
  ```
* **Celery Beat**:

  ```bash
  docker-compose logs -f beat
  ```

## Остановка и очистка

```bash
# Остановить сервисы
docker-compose down

# Удалить тома (данные PostgreSQL)
docker-compose down -v
```

## Git и вклад

* Домашняя работа — ветка `develop` → `main`.
* В `.gitignore`:

  ```gitignore
  .env
  __pycache__/
  *.pyc
  venv/
  .idea/
  ```
* Убедитесь, что в коммитах нет сгенерированных или чувствительных файлов.

---
## Запуск локально

1. **Клонировать репозиторий**  
   ```bash
   git clone https://github.com/anaromanova/Habits.git
   cd Habits
   git checkout develop
Установить зависимости


poetry install
Задать переменные окружения
Создайте файл .env в корне проекта, скопировав шаблон:


cp .env.example .env
и заполните его реальными значениями

Применить миграции и запустить


poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
Откройте в браузере: http://127.0.0.1:8000/

## Развёртывание на удалённом сервере
Мы используем виртуальную машину в Яндекс.Облаке с Ubuntu 24.04, Docker и Docker-Compose.

Создать ВМ в Yandex Cloud

Простой образ: Ubuntu 24.04 LTS

Ресурсы: 2 vCPU, 2 ГБ RAM, SSD 20 ГБ

Логин: ubuntu

Добавить ваш SSH-ключ

Подключиться по SSH


ssh ubuntu@89.169.172.251
Установить Docker & docker-compose


sudo apt update && sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
Клонировать репозиторий и собрать контейнеры


git clone https://github.com/anaromanova/Habits.git
cd Habits
git checkout develop
cp .env.example .env    # и заполнить переменные
docker-compose up -d --build
Проверить статус контейнеров


docker ps
Вы должны видеть сервисы: habits_web, habits_db, habits_redis, habits_worker, habits_beat.

Применить миграции и создать супер-юзера


docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py createsuperuser
Адрес продакшен-сервера
Ваше приложение доступно по адресу:

http://89.169.172.251/

Админка:

http://89.169.172.251/admin/

CI/CD с GitHub Actions
В папке .github/workflows/ci-cd.yml настроен pipeline:

Trigger: push в ветку develop

Steps:

Checkout

Setup Python

Установка зависимостей (poetry install)

Прогон тестов (poetry run pytest)

Сборка Docker-образа

Push образа в GitHub Package Registry (или Docker Hub)

Деплой на сервер через SSH (docker-compose pull && docker-compose up -d)

## Запуск вручную
При необходимости вы можете запустить workflow вручную на GitHub:
Actions → CI/CD → Run workflow.

# Полезные команды

# Локально
poetry run pytest
poetry run python manage.py test

# В Docker
docker-compose build
docker-compose up -d
docker-compose logs -f        # следить за логами
docker-compose exec web bash  # зайти внутрь контейнера
Важно: не забудьте хранить все секреты (SSH-ключи, API- токены, пароли) в GitHub Secrets или в переменных окружения сервера, а .env не коммитить в репозиторий.

.env
.idea/
__pycache__/
Спасибо за внимание!
