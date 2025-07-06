from celery import shared_task
from django.utils import timezone
from .models import Habit

@shared_task
def send_reminders():
    now = timezone.localtime()
    due_qs = (
        Habit.objects
        .filter(time__hour=now.hour, time__minute=now.minute)
        .select_related('user')
        .exclude(user__telegram_chat_id__isnull=True)
    )

    for habit in due_qs:
        chat_id = habit.user.telegram_chat_id
        # отправляем напоминание
        bot.send_message(chat_id=chat_id, text=f"Пора выполнить: {habit.title}")
