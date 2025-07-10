# habits/tasks.py
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from telegram import Bot

from .models import Habit


@shared_task
def send_habit_reminders():
    """
    Каждую минуту выбираем привычки, у которых поле `time`
    совпадает с текущим часом и минутой, и отправляем напоминание
    в чат, указанный в профиле пользователя.
    """
    now = timezone.localtime()
    hour = now.hour
    minute = now.minute

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    sent_count = 0

    qs = Habit.objects.filter(
        time__hour=hour,
        time__minute=minute,
        is_reward=False,
    ).select_related("user", "user__profile")

    for habit in qs:
        profile = getattr(habit.user, "profile", None)
        chat_id = getattr(profile, "telegram_chat_id", None)
        if not chat_id:
            continue

        text = (
            f"🔔 Напоминание о привычке:\n"
            f"• Действие: {habit.action}\n"
            f"• Время: {habit.time.strftime('%H:%M')}\n"
            f"• Место: {habit.place}"
        )
        try:
            bot.send_message(chat_id=chat_id, text=text)
            sent_count += 1
        except Exception:
            continue

    return f"Sent {sent_count} reminders at {hour:02d}:{minute:02d}"
