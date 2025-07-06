import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habits_project.config.settings')
app = Celery('habits_project.config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-habit-reminders-every-minute': {
        'task': 'habits_project.habits.tasks.send_reminders',
        'schedule': crontab(),  # каждую минуту
    },
}