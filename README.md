# Habits

Сервис трекинга привычек с напоминаниями в Telegram.

## Установка

```bash
git clone git@github.com:anaromanova/Habits.git
cd habits
poetry install
cp .env.example .env
# заполнить .env
poetry run python manage.py migrate