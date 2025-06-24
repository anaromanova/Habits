from celery import shared_task
from django.utils import timezone
from .models import Habit
from .services import send_telegram_message

@shared_task
def send_reminders():
    now = timezone.localtime()
    due = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)
    for habit in due:
        chat_id = getattr(habit.user.profile, 'telegram_chat_id', None)
        if chat_id:
            text = f"Напоминание: {habit.action} в {habit.time.strftime('%H:%M')} @ {habit.place}"
            send_telegram_message(chat_id, text)
